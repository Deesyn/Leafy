# MIT License
# Copyright (c) 2025 kenftr


import platform
from packaging import version
from Swit.src.loader.utils.GetPluginInfo import _get_plugin_info
def _check_python_version(plugin_path:None,plugin_ref:str) -> bool:
    if not plugin_path:
        _, _, required, _ = _get_plugin_info(None,plugin_ref, plugin_ref)
    else:
        _,_,required,_ = _get_plugin_info(plugin_path=plugin_path,plugin_object=None,plugin_name=None)
    if not required:
        return True

    py_ver = version.parse(platform.python_version())

    if required.startswith(">="):
        return py_ver >= version.parse(required.replace(">=", ""))
    if required.startswith("<="):
        return py_ver <= version.parse(required.replace("<=", ""))
    return True