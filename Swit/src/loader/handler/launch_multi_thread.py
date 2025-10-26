import threading
import os
import sys
import asyncio

from Swit.src.handler.file.config import Config
from Swit.src.handler.file.path_manager import path
from Swit.src.utils.logger import Logger
from Swit.src.utils.async_runner import run_async

from Swit.src.loader.load.LoadObject import Load_Cog
from Swit.src.loader.load.LoadMapping import _load_mapping
from Swit.src.loader.utils.CheckPythonVersion import _check_python_version
async def _handler(app,plugin):

    #flag
    is_er = False

    for plugin_name in plugin:
        try:
            Logger.LOADER(f"Load plugin: {plugin_name}")
            sys.path.insert(0, os.path.join(path.plugin(), plugin_name))
            mapping = _load_mapping(None,plugin_name)
            mapping_config = Config.Mapping()
            mapping_paths = mapping["mapping"]["path"]

            prefix_path = mapping_paths["prefix_command_path"]
            slash_path = mapping_paths["slash_command_path"]
            event_path = mapping_paths["event_command_path"]
            command_group_path = mapping_paths["command_group_path"]

            prefix_commands = mapping["mapping"]["prefix_command_list"]
            slash_commands = mapping["mapping"]["slash_command_list"]
            event_commands = mapping["mapping"]["events_list"]
            group_commands = mapping["mapping"]["command_group_list"]
            if mapping_config['format'] != mapping['mapping']['format']:
                Logger.LOADER(
                    f"Plugin {plugin_name} uses {mapping['mapping']['format']} format instead of required {mapping_config['format']}. Skipping...")
                return
            if not _check_python_version(plugin_name, plugin_name=plugin_name):
                Logger.WARN(f"Skipped {plugin_name} (Python version incompatible)")
                return
            if Config.Loader.fast_module():
                await asyncio.gather(
                    Load_Cog(app, prefix_path, plugin_name, "prefix", prefix_commands),
                    Load_Cog(app, slash_path, plugin_name, "slash", slash_commands),
                    Load_Cog(app, event_path, plugin_name, "event", event_commands),
                    Load_Cog(app, command_group_path, plugin_name, "group", group_commands)
                )
            else:
                await Load_Cog(app, prefix_path, plugin_name, "prefix", prefix_commands)
                await Load_Cog(app, prefix_path, plugin_name, "slash", prefix_commands)
                await Load_Cog(app, prefix_path, plugin_name, "event", prefix_commands)
                await Load_Cog(app, prefix_path, plugin_name, "group", prefix_commands)

        except Exception as e:
            sys.path.remove(os.path.join(path.plugin(), plugin_name))
            Logger.ERROR(message=f"Failed to load {plugin_name}! Skip")
            is_er = True
        finally:
            if is_er == False:
                sys.path.remove(os.path.join(path.plugin(), plugin_name))

def _launch_multi_thread(app,plugin_list,total_thread,plugin_per_thread):
    threads = []
    for i in range(0,len(plugin_list),plugin_per_thread):
        plugin_group = plugin_list[i:i+plugin_per_thread]
        t = threading.Thread(target=run_async,args=(_handler(app,plugin_group),))
        threads.append(t)
        if len(threads) > total_thread:
            break
    for t in threads:
        t.start()
