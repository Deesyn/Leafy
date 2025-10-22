# MIT License
# Copyright (c) 2025 kenftr

# Built-in Imports
import os
import sys
import asyncio
from typing import Optional

# Third-Party
from discord.ext import commands

# Swit Utility Imports
from Swit.src.utils.logger import Logger
from Swit.src.utils.calculator.thread_calculator import thread_calculator
from Swit.src.handler.file.config import Config
from Swit.src.handler.file.extract import extract
from Swit.src.handler.file.log import log
from Swit.src.handler.file.path_manager import path

# Swit Loader Imports
from Swit.src.loader.load.load_object import _load_object
from Swit.src.loader.load.load_mapping import _load_mapping
from Swit.src.loader.load.load_main_event import _load_main_event
from Swit.src.loader.utils.get_plugin_info import _get_plugin_info
from Swit.src.loader.utils.check_python_version import _check_python_version
from Swit.src.loader.handler.launch_multi_thread import _launch_multi_thread
from Swit.src.loader.handler.download_package import download_package

# Swit Terminal Imports
from Swit.src.core.terminal import print_plugin_dir_tree

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



    async def _load_plugin(self, plugin_name: str, plugin_object):
        try:
            Logger.LOADER(f"Load plugin: {plugin_name}")
            sys.path.insert(0, os.path.join(path.plugin(), plugin_name))
            mapping = _load_mapping(plugin_name, plugin_object)
            mapping_config = Config.Mapping()
            mapping_paths = mapping["mapping"]["path"]

            prefix_path = mapping_paths["prefix_command_path"]
            slash_path = mapping_paths["slash_command_path"]
            event_path = mapping_paths["event_command_path"]
            command_group_path = mapping_paths["command_group_path"]

            prefix_commands = mapping["mapping"]["prefix_command_list"]
            slash_commands = mapping["mapping"]["slash_command_list"]
            event = mapping["mapping"]["events_list"]
            group_commands = mapping["mapping"]["command_group_list"]

            _,_,_,self.packages_list = _get_plugin_info(plugin_name=plugin_name, plugin_object=plugin_name)
            download_package(package_list=self.packages_list)

            if mapping_config['format'] != mapping['mapping']['format']:
                Logger.LOADER(f"Plugin {plugin_name} uses {mapping['mapping']['format']} format instead of required {mapping_config['format']}. Skipping...")
                return
            if not _check_python_version(plugin_name, plugin_object):
                Logger.WARN(f"Skipped {plugin_name} (Python version incompatible)")
                return
            tasks = []

            if self.allow_prefix:
                tasks.append(_load_object(self.app,prefix_path,plugin_name, "prefix", prefix_commands))
            if self.allow_slash:
                tasks.append(_load_object(self.app,slash_path,plugin_name, "slash", slash_commands))
            if self.allow_events:
                tasks.append(_load_object(self.app,event_path,plugin_name, "event", event))
            if self.allow_group:
                tasks.append(_load_object(self.app,command_group_path,plugin_name, "group", group_commands))


            if Config.Loader.fast_module():
                await asyncio.gather(*tasks)
            else:
                for task in tasks:
                    await task

        except Exception as e:
            sys.path.remove(os.path.join(path.plugin(), plugin_name))
            Logger.ERROR(message=f"Failed to load {plugin_name}! Skip")
            traceback_log_path = log.write_bug(e)
            Logger.LOADER(message=f'The bug details are saved at {traceback_log_path}')
        finally:
            sys.path.remove(os.path.join(path.plugin(), plugin_name))
            Logger.INFO(message=f'Load {plugin_name} success!')


    async def start_loader(self):
        plugin_list = [f for f in os.listdir(path.plugin()) if f != 'plugin_configs']
        len_plugin_list = len(plugin_list)
        Logger.INFO("Loading...")
        print_plugin_dir_tree(plugin_list=plugin_list)
        Logger.INFO(f"Total plugin: {len_plugin_list}")
        if Config.Loader.multi_thread() == True:
            data = thread_calculator(plugins_list=plugin_list)
            total_thread = data['total_thread']
            plugin_per_thread = data['plugin_per_thread']
            _launch_multi_thread(app=self.app,plugin_list=plugin_list,total_thread=total_thread,plugin_per_thread=plugin_per_thread)
        else:
            for plugin in os.listdir(path.plugin()):
                if plugin == "Plugin configs":
                    continue
                if plugin.endswith(".dis") or plugin.endswith('.disable'):
                    continue
                file_path = os.path.join(path.plugin(), plugin)

                if plugin.endswith(".zip"):
                    data = extract.zip(file_path)
                    await self._load_plugin(plugin_name=plugin,
                                            plugin_object=plugin)
                    await _load_main_event("archive", plugin, data)

                elif plugin.endswith(".rar"):
                    data = extract.rar(file_path)
                    await self._load_plugin(plugin_name=plugin,
                                            plugin_object=plugin)
                    await _load_main_event("archive", plugin, data)

                elif os.path.isdir(file_path):
                    await self._load_plugin(plugin_name= plugin,
                                            plugin_object= plugin)
                    await _load_main_event("dir", plugin, plugin)
