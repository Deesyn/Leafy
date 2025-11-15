import os
import sys
import asyncio
from Swit.sdk.api import App
from Swit.src.utils.Logger import Logger

async def _load_main_event(plugin_type: str, plugin_name: str, plugin_source):
    from Swit.src.handler.file.path_manager import path
    from Swit.src.loader.load.LoadMapping import _load_mapping
    from Swit.src.utils.LoaderUtils.ImportModule import _import_module


    mapping = _load_mapping(
        plugin_path=None,
        plugin_ref=plugin_name if plugin_type == "dir" else None,
        plugin_object=plugin_source
    )
    if not mapping:
        return
    Logger.DEBUG(f"Loading main event for plugin: {plugin_name}")
    mod_info = mapping.get("module", {}).get('main_event', {})

    event_file = mod_info.get("event_file_name")
    start_func_name = mod_info.get("start_function")
    init_variable = mod_info.get('init_variable', {})
    if str(plugin_name).endswith('.zip'):
        print(plugin_name)
        plugin_path = os.path.join(str(path.root()),'cache','plugin_extract',str(plugin_name).split('.')[0])
    else:
        plugin_path = os.path.join(path.plugin(), plugin_name)
    sys.path.insert(0, plugin_path)
    Logger.DEBUG(f"Inserted plugin path into sys.path: {plugin_path}")

    module_name = event_file.replace(".py", "")
    module_path = os.path.join(plugin_path, event_file)
    module = _import_module(plugin_path=plugin_path, module_name=module_name, module_path=str(module_path))
    Logger.DEBUG(f"Imported module {module_name} from {module_path}")

    try:
        function = getattr(module, start_func_name, None)
        if not function:
            Logger.DEBUG(f"Start function {start_func_name} not found in {module_name}")
            return

        parms = {}
        for key, api in init_variable.items():
            if api.lower() == 'swit.app':
                parms[key] = App.get_app()
        Logger.DEBUG(f"Prepared function parameters: {parms}")

        if asyncio.iscoroutinefunction(function):
            Logger.DEBUG(f"Calling async function: {start_func_name}")
            await function(**parms)
        else:
            Logger.DEBUG(f"Calling sync function: {start_func_name}")
            function(**parms)
        Logger.DEBUG(f"Successfully executed function: {start_func_name}")

    except Exception as e:
        Logger.DEBUG(f"Error while executing function {start_func_name}: {e}")
        raise RuntimeError(e)
    finally:
        sys.path.remove(plugin_path)
        Logger.DEBUG(f"Removed plugin path from sys.path: {plugin_path}")
