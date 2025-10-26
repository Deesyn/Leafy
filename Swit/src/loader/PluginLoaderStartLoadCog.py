# MIT License
# Copyright (c) 2025 kenftr

import asyncio, os
from Swit.src.loader.load.LoadObject import Load_Cog
from Swit.src.loader.load.LoadMapping import _load_mapping
from Swit.src.handler.file.config import Config


async def start_load_cog(self, extract_path: None, plugin_name: None):

    if extract_path:
        mapping_data = _load_mapping(plugin_path=os.path.join(str(extract_path), str(plugin_name)), plugin_ref=None,
                                     plugin_object=None)
    else:
        mapping_data = mapping_data = _load_mapping(None, plugin_ref=plugin_name, plugin_object=None)
    mapping_paths = mapping_data["mapping"]["path"]
    prefix_path = mapping_paths["prefix_command_path"]
    slash_path = mapping_paths["slash_command_path"]
    event_path = mapping_paths["event_command_path"]
    command_group_path = mapping_paths["command_group_path"]

    prefix_commands = mapping_data["mapping"]["prefix_command_list"]
    slash_commands = mapping_data["mapping"]["slash_command_list"]
    events = mapping_data["mapping"]["events_list"]
    group_commands = mapping_data["mapping"]["command_group_list"]
    tasks = []
    if self.allow_prefix:
        tasks.append(Load_Cog(self.app, prefix_path, plugin_name, "prefix", prefix_commands))
    if self.allow_slash:
        tasks.append(Load_Cog(self.app, slash_path, plugin_name, "slash", slash_commands))
    if self.allow_events:
        tasks.append(Load_Cog(self.app, event_path, plugin_name, "event", events))
    if self.allow_group:
        tasks.append(Load_Cog(self.app, command_group_path, plugin_name, "group", group_commands))

    if Config.Loader.fast_module():
        await asyncio.gather(*tasks)
    else:
        for task in tasks:
            await task