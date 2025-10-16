import os
import sys
import asyncio
from Leafy.LeafySDK.api import App
async def _load_main_event(plugin_type: str, plugin_name: str, plugin_source):

    from Leafy.src.utils.file_handler.path_manager import path
    from Leafy.src.loader.load.load_mapping import _load_mapping
    from Leafy.src.loader.utils.import_module import _import_module

    mapping = _load_mapping(plugin_name= plugin_name if plugin_type == "dir" else None,
                            plugin_source= plugin_source)
    mod_info = mapping.get("module", {}).get('main_event',{})

    event_file = mod_info.get("event_file_name")
    start_func_name = mod_info.get("start_function")
    stop_func_name = mod_info.get("stop_function")
    init_variable = mod_info.get('init_variable')

    sys.path.insert(0, os.path.join(path.plugin(), plugin_name))
    module_name = event_file.replace(".py", "")
    module_path = os.path.join(path.plugin(),plugin_name,event_file)
    module = _import_module(module_name,str(module_path))

    for function_name in [start_func_name, stop_func_name]:
        function = getattr(module, function_name, None)
        parms = {}
        for key, api in init_variable:
            if api.lower() == 'leaf.app':
                parms[key] = App.get_app()
        if function:
            try:
                if asyncio.iscoroutinefunction(function):
                    await function(**parms)
                else:
                    function(**parms)
            except Exception as e:
                raise RuntimeError(e)
    sys.path.remove(os.path.join(path.plugin(), plugin_name))