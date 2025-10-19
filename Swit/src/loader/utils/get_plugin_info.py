from functools import lru_cache
from Swit.src.loader.load.load_mapping import _load_mapping

def _get_plugin_info(plugin_name: str, plugin_object):
    data = _load_mapping(plugin_name, plugin_object)
    return (
        data.get("name"),
        data.get("version"),
        data.get("require", {}).get("python_version"),
        data.get("require",{}).get('packages', None)
    )