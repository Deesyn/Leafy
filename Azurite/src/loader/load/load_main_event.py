import os
import sys
import asyncio
import importlib
from Azurite.src.loader.load._load_mapping import _load_mapping
from Azurite.src.utils.path_manager import path
async def _load_main_event(plugin_type: str, plugin_name: str, plugin_source):
    mapping = _load_mapping(plugin_name= plugin_name if plugin_type == "dir" else None,
                            plugin_source= plugin_source)
    mod_info = mapping.get("module", {})

    event_file = mod_info.get("event_file_name")
    start_func_name = mod_info.get("start_function")
    stop_func_name = mod_info.get("stop_function")

    sys.path.insert(0, os.path.join(path.plugin(), plugin_name))
    module_name = event_file.replace(".py", "")
    module = importlib.import_module(module_name)

    for function_name in [start_func_name, stop_func_name]:
        function = getattr(module, function_name, None)
        if function:
            try:
                if asyncio.iscoroutinefunction(function):
                    await function()
                else:
                    function()
            except Exception as e:
                raise RuntimeError(e)