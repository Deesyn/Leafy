# MIT License
# Copyright (c) 2025 kenftr
import os
import sys
import asyncio
from typing import Optional
from discord.ext import commands

from Azurite.src.utils.config import Config
from Azurite.src.utils.extract import extract
from Azurite.src.utils.path_manager import path
from Azurite.src.utils.Local_Logger import Logger
from Azurite.src.utils.thread_calculator import thread_calculator

from Azurite.src.loader.load.load_object import _load_object
from Azurite.src.loader.load._load_mapping import _load_mapping
from Azurite.src.loader.load.load_main_event import _load_main_event
from Azurite.src.loader.utils.check_python_version import _check_python_version
from Azurite.src.loader.utils.multil_thread_handler import multil_thread_handler


class Loader:
    def __init__(self, app):
        self.app: Optional[commands.Bot] = app

        # Loader settings
        self.multi_thread = Config.Loader.multi_thread()
        self.max_thread = Config.Loader.max_thread()
        self.timeout = Config.Loader.timed_out()

        # Allow settings
        self.allow_prefix = Config.Loader.Allow.prefix_command()
        self.allow_slash = Config.Loader.Allow.slash_command()
        self.allow_group = Config.Loader.Allow.group_command()
        self.allow_events = Config.Loader.Allow.events()
        self.allowed_formats = Config.Loader.Allow.plugin_format()

        # Script loader settings
        self.script_loader_enabled = Config.Loader.ScriptLoader.status()
        self.disabled_scripts = Config.Loader.ScriptLoader.disable_script_list()



    async def _load_plugin(self, plugin_name: str, plugin_source):
        try:
            Logger.LOADER(f"Load plugin: {plugin_name}")
            sys.path.insert(0, os.path.join(path.plugin(), plugin_name))
            mapping = _load_mapping(plugin_name, plugin_source)
            mapping_config = Config.Mapping()
            mapping_paths = mapping["mapping"]["path"]

            self.prefix_path = mapping_paths["prefix_command_path"]
            self.slash_path = mapping_paths["slash_command_path"]
            self.event_path = mapping_paths["event_command_path"]
            self.command_group_path = mapping_paths["command_group_path"]

            self.prefix_commands = mapping["mapping"]["prefix_command_list"]
            self.slash_commands = mapping["mapping"]["slash_command_list"]
            self.event = mapping["mapping"]["events_list"]
            self.group_commands = mapping["mapping"]["command_group_list"]
            if mapping_config['format'] != mapping['mapping']['format']:
                Logger.LOADER(f"Plugin {plugin_name} uses {mapping['mapping']['format']} format instead of required {mapping_config['format']}. Skipping...")
                return
            if not _check_python_version(plugin_name, plugin_source):
                Logger.WARN(f"Skipped {plugin_name} (Python version incompatible)")
                return
            tasks = []
            if self.allow_prefix:
                tasks.append(_load_object(self.app,self.prefix_path,plugin_name, "prefix", self.prefix_commands))
            if self.allow_slash:
                tasks.append(_load_object(self.app,self.slash_path,plugin_name, "slash", self.slash_commands))
            if self.allow_events:
                tasks.append(_load_object(self.app,self.event_path,plugin_name, "event", self.event))
            if self.allow_group:
                tasks.append(_load_object(self.app,self.command_group_path,plugin_name, "group", self.group_commands))
            if Config.Loader.fast_module():
                await asyncio.gather(*tasks)
            else:
                if self.allow_prefix:
                    await _load_object(self.app, self.prefix_path, plugin_name, "prefix", self.prefix_commands)
                if self.allow_slash:
                    await _load_object(self.app, self.slash_path, plugin_name, "slash", self.slash_commands)
                if self.allow_events:
                    await _load_object(self.app, self.event_path, plugin_name, "event", self.event)
                if self.allow_group:
                    await _load_object(self.app, self.command_group_path, plugin_name, "group", self.group_commands)

        except Exception as e:
            sys.path.remove(os.path.join(path.plugin(), plugin_name))
            Logger.ERROR(message=f"Failed to load {plugin_name}! Skip")
            raise e
        finally:
            sys.path.remove(os.path.join(path.plugin(), plugin_name))


    async def start_loader(self):
        plugin_list = [f for f in os.listdir(path.plugin())]
        len_plugin_list = len(plugin_list)
        Logger.INFO("Loading...")
        for i, plugin in enumerate(plugin_list):
            if i < len(plugin_list) - 1:
                Logger.INFO(f"├── {plugin}")
            else:
                Logger.INFO(f"└── {plugin}")
        Logger.INFO(f"Total plugin: {len_plugin_list}")
        if Config.Loader.max_thread() == True:
            data = thread_calculator(plugins_list=plugin_list)
            total_thread = data['total_thread']
            plugin_per_thread = data['plugin_per_thread']
            multil_thread_handler(app=self.app,plugin_list=plugin_list,total_thread=total_thread,plugin_per_thread=plugin_per_thread)
        else:
            for file in os.listdir(path.plugin()):
                file_path = os.path.join(path.plugin(), file)

                if file.endswith(".zip"):
                    data = extract.zip(file_path)
                    await _load_main_event("archive", file, data)
                    await self._load_plugin(plugin_name=file,
                                            plugin_source=file)

                elif file.endswith(".rar"):
                    data = extract.rar(file_path)
                    await _load_main_event("archive", file, data)
                    await self._load_plugin(plugin_name=file,
                                            plugin_source=file)

                elif os.path.isdir(file_path):
                    await _load_main_event("dir", file, file)
                    await self._load_plugin(plugin_name= file,
                                            plugin_source= file)
