# MIT License
# Copyright (c) 2025 kenftr


def _import_module(plugin_path,module_name:str,module_path:str):
    import importlib.util
    import sys
    if str(plugin_path).endswith('.zip') or str(plugin_path).endswith('.rar'):
        sys.path.insert(0,plugin_path)
        module = importlib.import_module(module_name)
        sys.path.remove(plugin_path)
        return module

    spec = importlib.util.spec_from_file_location(module_name,module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module