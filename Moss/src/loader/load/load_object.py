import os
import json
import inspect
import importlib
from discord.ext import commands
from Moss.src.utils.file_handler.path_manager import path
async def _load_object(app: commands.Bot,cog_path,
                       plugin_name: str, path_name: str,
                       command_list: list):

    for item in command_list:
        try:
            file_name = item["file_name"].replace(".py", "")
            class_name = item["class"]

            if path_name == 'slash':
                module = importlib.import_module(f"{cog_path}.{file_name}")
            cls = getattr(module, class_name)
            params = {}

            custom_map_cfg = item.get("custom_mapping", {})
            if custom_map_cfg.get("enable"):
                mapping_path = os.path.join(
                    path.plugin(),
                    plugin_name,
                    "custom_mapping",
                    custom_map_cfg["path"]
                )

                if not os.path.exists(mapping_path):
                    continue

                with open(mapping_path, "r", encoding="utf-8") as f:
                    mapping_data = json.load(f)

                if mapping_data["init"]["enabled"]:
                    sig = inspect.signature(cls)
                    for key, val in mapping_data["init"]["variables"].items():
                        if key in sig.parameters:
                            if val.lower() == "azurite.bot":
                                params[key] = app
                            else:
                                params[key] = None
            if path_name == 'prefix':
                await app.add_cog(cls(**params))
            if path_name == "slash":
                await app.add_cog(cls(**params))
            elif path_name == "event":
                await app.add_cog(cls(**params))
            elif path_name == "group":
                await app.tree.add_command(cls(**params))


        except Exception as e:
            raise e