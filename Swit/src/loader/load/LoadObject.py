# MIT License
# Copyright (c) 2025 kenftr


import os
import json
import inspect
import importlib
import traceback
from discord.ext import commands
from Swit.src.handler.file.path_manager import path
from Swit.src.handler.file.log import log
from Swit.src.utils.logger import Logger

async def Load_Cog(
        app: commands.Bot,
        cog_path,
        plugin_name: str,
        path_name: str,
        command_list: list):
    """
    Dynamically loads and registers Discord cogs or commands into a Bot instance.

    This function iterates over a list of command definitions, imports their modules,
    initializes classes with optional custom mappings, and adds them to the bot either
    as prefix commands, slash commands, event handlers, or command groups.

    It also supports loading configuration from JSON mapping files to provide
    parameters when initializing the cog classes.

    app : commands.Bot
        The Discord Bot instance to which cogs/commands will be added.
    cog_path : str
        Python module path where the cog files are located.
        Example: "Swit.src.cogs".
    plugin_name : str
        Name of the plugin folder, used to locate optional custom mapping files.
    path_name : str
        The type of registration for the cog/command. Supported values:
        - "prefix" : regular prefix command
        - "slash"  : slash command
        - "event"  : event listener
        - "group"  : command group
    command_list : list of dict
        A list of dictionaries describing each cog/command to load. Each dictionary may contain:
        - "file_name" : str, name of the Python file (required)
        - "class"     : str, name of the class to instantiate (required)
        - "custom_mapping" : dict, optional mapping configuration with keys:
            - "enable" : bool, whether to use custom mapping
            - "path"   : str, relative path to the JSON mapping file

    Exception
        Any exception during import, class initialization, or registration is caught.
        Traceback is logged via `log.write_bug`. Non-awaited coroutine warnings are ignored.

    - Files not ending with `.py` are skipped.
    - If a custom mapping JSON is provided and `init.enabled` is True, the class
      constructor will receive parameters based on the mapping.
    - The function logs debug information at each significant step via `Logger.DEBUG`.
    """

    for item in command_list:
        try:
            if not item["file_name"].endswith('.py'):
                Logger.DEBUG(f"Skipped non-Python file: {item['file_name']}")
                return

            file_name = item["file_name"].replace(".py", "")
            class_name = item["class"]
            Logger.DEBUG(f"Preparing to import {cog_path}.{file_name}")
            module = importlib.import_module(f"{cog_path}.{file_name}")
            Logger.DEBUG(f'Imported module: {cog_path}.{file_name}')
            cls = getattr(module, class_name)
            Logger.DEBUG(f'Got class: {class_name}')
            params = {}

            custom_map_cfg = item.get("custom_mapping", {})
            if custom_map_cfg.get("enable"):
                mapping_path = os.path.join(
                    path.plugin(),
                    plugin_name,
                    "custom_mapping",
                    custom_map_cfg["path"]
                )
                Logger.DEBUG(f"Custom mapping enabled, path: {mapping_path}")

                if not os.path.exists(mapping_path):
                    Logger.DEBUG(f"Mapping path does not exist: {mapping_path}")
                    continue

                with open(mapping_path, "r", encoding="utf-8") as f:
                    mapping_data = json.load(f)
                Logger.DEBUG(f"Loaded mapping data from {mapping_path}")

                if mapping_data["init"]["enabled"]:
                    sig = inspect.signature(cls)
                    for key, val in mapping_data["init"]["variables"].items():
                        if key in sig.parameters:
                            if val.lower() == "swit.bot":
                                params[key] = app
                            else:
                                params[key] = None
                    Logger.DEBUG(f"Prepared init params: {params}")

            Logger.DEBUG(f"Adding cog/command: {class_name} under path: {path_name}")
            if path_name == 'prefix':
                await app.add_cog(cls(**params))
            if path_name == "slash":
                await app.add_cog(cls(**params))
            elif path_name == "event":
                await app.add_cog(cls(**params))
            elif path_name == "group":
                await app.tree.add_command(cls(**params))
            Logger.DEBUG(f"Successfully added: {class_name}")

        except Exception as e:
            if 'was never awaited' not in str(e):
                return
            traceback_log_path = log.write_bug(traceback.format_exc())
            Logger.LOADER(message=f'The bug details are saved at {traceback_log_path}')
