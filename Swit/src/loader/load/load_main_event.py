import os
import sys
import asyncio
from Swit.SwitSDK.api import App
async def _load_main_event(plugin_type: str, plugin_name: str, plugin_source):

    from Swit.src.handler.file.path_manager import path
    from Swit.src.loader.load.load_mapping import _load_mapping
    from Swit.src.loader.utils.import_module import _import_module

    mapping = _load_mapping(plugin_name= plugin_name if plugin_type == "dir" else None, plugin_object= plugin_source)
    mod_info = mapping.get("module", {}).get('main_event',{})

    event_file = mod_info.get("event_file_name")
    start_func_name = mod_info.get("start_function")
    init_variable = mod_info.get('init_variable')

    sys.path.insert(0, os.path.join(path.plugin(), plugin_name))
    module_name = event_file.replace(".py", "")
    module_path = os.path.join(path.plugin(),plugin_name,event_file)
    plugin_path = os.path.join(path.plugin(),plugin_name)
    module = _import_module(plugin_path=plugin_path,module_name=module_name,module_path=str(module_path))

    for function_name in [start_func_name]:
        function = getattr(module, function_name, None)
        parms = {}
        for key, api in init_variable.items():
            if api.lower() == 'swit.app':
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