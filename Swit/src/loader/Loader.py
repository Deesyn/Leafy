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


    async def _load_plugin(self,plugin_type, plugin_name: str):

        #flag
        is_er = False

        if plugin_type.endswith('.zip'):
            try:
                full_plugin_path = os.path.join(path.plugin(),plugin_name)
                extract_path  = os.path.join(path.root(),'cache','plugin_extract')

                os.makedirs(extract_path,exist_ok=True)

                plugin_name = str(plugin_name).split('.')[0]

                sys.path.insert(0, os.path.join(extract_path,plugin_name))

                with zipfile.ZipFile(full_plugin_path,'r') as z:
                    z.extractall(path=os.path.join(extract_path,str(plugin_name).split('.')[0]))
                Logger.LOADER(f"Extract success: {plugin_name}")
                try:
                    Logger.LOADER(f"Load plugin: {plugin_name}")
                    sys.path.insert(0,os.path.join(extract_path,plugin_name))
                    prepare(plugin_path=os.path.join(str(extract_path),str(plugin_name)),plugin_name=plugin_name)
                    await start_load_cog(self,extract_path,plugin_name)

                except Exception as e:
                    Logger.ERROR(message=f"Failed to load {plugin_name}! Skip")
                    traceback_log_path = log.write_bug(traceback.format_exc())
                    Logger.LOADER(message=f'The bug details are saved at {traceback_log_path}')
            except Exception as e:
                Logger.ERROR(f"Failed to extract plugin {plugin_name}!")
                traceback_log_path = log.write_bug(traceback.format_exc())
                Logger.LOADER(message=f'The bug details are saved at {traceback_log_path}')

        if plugin_type == 'dir':
            try:
                Logger.LOADER(f"Load plugin: {plugin_name}")
                sys.path.insert(0, os.path.join(path.plugin(), plugin_name))

                _,_,_,self.packages_list = _get_plugin_info(None,plugin_name=plugin_name, plugin_object=plugin_name)
                download_package(package_list=self.packages_list)

                prepare(plugin_path=None,plugin_name=plugin_name)
                await start_load_cog(self,extract_path=None,plugin_name=plugin_name)


            except Exception as e:
                is_er = True
                sys.path.remove(os.path.join(path.plugin(), plugin_name))
                Logger.ERROR(message=f"Failed to load {plugin_name}! Skip")
                traceback_log_path = log.write_bug(data=str(e))
                Logger.LOADER(message=f'The bug details are saved at {traceback_log_path}')
            finally:
                if is_er == False:
                    sys.path.remove(os.path.join(path.plugin(), plugin_name))
                    Logger.INFO(message=f'Load {plugin_name} success!')



    async def start_loader(self):
        plugins = [plugin for plugin in os.listdir(path.plugin()) if plugin != 'Plugin configs']
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
