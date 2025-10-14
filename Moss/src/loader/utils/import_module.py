def _import_module(module_name:str,module_path:str):
    import importlib.util
    spec = importlib.util.spec_from_file_location(module_name,module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module