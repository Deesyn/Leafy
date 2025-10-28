# MIT License
# Copyright (c) 2025 kenftr

# Built-in Imports
import os
import sys
import asyncio
from typing import Optional
import zipfile
import traceback
# Third-Party
import rarfile
from discord.ext import commands

# Swit Utility Imports
from Swit.src.utils.logger import Logger
from Swit.src.utils.calculator.thread_calculator import thread_calculator
from Swit.src.handler.file.config import Config
from Swit.src.handler.file.extract import extract
from Swit.src.handler.file.log import log
from Swit.src.handler.file.path_manager import path
from Swit.src.handler.cache import Cache

# Swit Loader Imports
from Swit.src.loader.load.LoadMainEvent import _load_main_event
from Swit.src.loader.utils.GetPluginInfo import _get_plugin_info
from Swit.src.loader.PluginLoaderPrepare import prepare
from Swit.src.loader.handler.launch_multi_thread import _launch_multi_thread
from Swit.src.loader.handler.download_package import download_package
from Swit.src.loader.PluginLoaderStartLoadCog import start_load_cog
# Swit Terminal Imports
from Swit.src.core.terminal import print_plugin_dir_tree



class PluginLoader:
    def __init__(self, app):
        self.app: Optional[commands.Bot] = app

        self.multi_thread = Config.Loader.multi_thread()
        self.max_thread = Config.Loader.max_thread()
        self.timeout = Config.Loader.timed_out()

        self.allow_prefix = Config.Loader.Allow.prefix_command()
        self.allow_slash = Config.Loader.Allow.slash_command()
        self.allow_group = Config.Loader.Allow.group_command()
        self.allow_events = Config.Loader.Allow.events()
        self.allowed_formats = Config.Loader.Allow.plugin_format()

        self.script_loader_enabled = Config.Loader.ScriptLoader.status()
        self.disabled_scripts = Config.Loader.ScriptLoader.disable_script_list()

    async def _load_plugin(self, plugin_type, plugin_name: str):
        if plugin_type.endswith('.zip'):
            try:
                cache_file_name = 'extract_plugin_list'
                Cache.create(file=cache_file_name)
                Cache_file_data = str(Cache.read(file=cache_file_name)).split('\n')
                Logger.DEBUG(f"Loaded cache file data: {Cache_file_data}")

                full_plugin_path = os.path.join(path.plugin(), plugin_name)
                extract_path = os.path.join(path.root(), 'cache', 'plugin_extract')
                Logger.DEBUG(f"Plugin zip path: {full_plugin_path}")
                Logger.DEBUG(f"Extraction path: {extract_path}")

                os.makedirs(extract_path, exist_ok=True)
                plugin_base_name = str(plugin_name).split('.')[0]

                sys.path.insert(0, os.path.join(extract_path, plugin_base_name))
                Logger.DEBUG(f"Added to sys.path: {os.path.join(extract_path, plugin_base_name)}")

                if plugin_base_name not in Cache_file_data:
                    Logger.DEBUG(f"Plugin {plugin_base_name} not in cache. Extracting...")
                    with zipfile.ZipFile(full_plugin_path, 'r') as z:
                        z.extractall(path=os.path.join(extract_path, plugin_base_name))
                        Logger.DEBUG(f"Extracted files: {z.namelist()}")
                        Logger.DEBUG(f"Total files extracted: {len(z.namelist())}")
                        Cache.write(file=cache_file_name, data=f"{plugin_base_name}\n", append=True)
                    Logger.LOADER(f"Extract success: {plugin_base_name}")
                else:
                    Logger.DEBUG(f"Plugin {plugin_base_name} already extracted. Skipping extraction.")

                try:
                    Logger.LOADER(f"Loading plugin: {plugin_base_name}")
                    prepare(plugin_path=os.path.join(extract_path, plugin_base_name),
                            plugin_name=plugin_base_name)
                    await start_load_cog(self, extract_path, plugin_base_name)
                    Logger.DEBUG(f"Plugin {plugin_base_name} added to cache")
                except Exception as e:
                    Logger.ERROR(f"Failed to load plugin {plugin_base_name}! Skip")
                    traceback_log_path = log.write_bug(traceback.format_exc())
                    Logger.LOADER(f"The bug details are saved at {traceback_log_path}")
                    Logger.DEBUG(e)
            except Exception as e:
                Logger.ERROR(f"Failed to extract plugin {plugin_name}!")
                traceback_log_path = log.write_bug(traceback.format_exc())
                Logger.LOADER(f"The bug details are saved at {traceback_log_path}")
                Logger.DEBUG(e)


    async def start_loader(self):
        plugins = [
            plugin for plugin in os.listdir(path.plugin())
            if plugin != 'Plugin configs' and not (plugin.endswith('.disable') or plugin.endswith('.dis'))
        ]
        Logger.INFO("Loading...")
        print_plugin_dir_tree(plugin_list=plugins)
        Logger.INFO(f"Discovered: {len(plugins)}" + ' plugin' if len(plugins) < 2 else ' plugins')
        if Config.Loader.multi_thread() == True:

            thread = thread_calculator(plugins_list=plugins)
            total_thread = thread['total_thread']
            plugin_per_thread = thread['plugin_per_thread']
            _launch_multi_thread(app=self.app,plugin_list=plugins,total_thread=total_thread,plugin_per_thread=plugin_per_thread)

        else:

            for plugin in plugins:
                file_path = os.path.join(path.plugin(), plugin)

                if plugin.endswith(".zip"):
                    data = extract.zip(file_path)
                    await self._load_plugin(plugin_type='.zip',plugin_name=plugin)
                    await _load_main_event("archive", plugin, data)

                elif plugin.endswith(".rar"):
                    data = extract.rar(file_path)
                    await self._load_plugin(plugin_type='.rar',plugin_name=plugin)
                    await _load_main_event("archive", plugin, data)

                elif os.path.isdir(file_path):
                    await self._load_plugin(plugin_type='dir',plugin_name= plugin)
                    await _load_main_event("dir", plugin, plugin)
