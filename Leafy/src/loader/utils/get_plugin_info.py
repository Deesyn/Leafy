from functools import lru_cache
from Leafy.src.loader.load.load_mapping import _load_mapping

def _get_plugin_info(plugin_name: str, plugin_source):
    data = _load_mapping(plugin_name, plugin_source)
    return (
        data.get("name"),
        data.get("version"),
        data.get("require", {}).get("python_version"),
        data.get("require",{}).get('packages', None)
    )