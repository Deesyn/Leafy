import platform
from packaging import version
from Leafy.src.loader.utils.get_plugin_info import _get_plugin_info
def _check_python_version(plugin_name: str, plugin_source) -> bool:
    _, _, required, _ = _get_plugin_info(plugin_name, plugin_source)
    if not required:
        return True

    py_ver = version.parse(platform.python_version())

    if required.startswith(">="):
        return py_ver >= version.parse(required.replace(">=", ""))
    if required.startswith("<="):
        return py_ver <= version.parse(required.replace("<=", ""))
    return True