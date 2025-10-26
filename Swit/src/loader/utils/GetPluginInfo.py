from functools import lru_cache
from Swit.src.loader.load.LoadMapping import _load_mapping

def _get_plugin_info(plugin_path:None,plugin_name: str, plugin_object):
    if not plugin_path:
        data = _load_mapping(None,plugin_name, plugin_object)
    else:
        data = _load_mapping(plugin_path=plugin_path,plugin_ref=None,plugin_object=None)
    return (
        data.get("name"),
        data.get("version"),
        data.get("require", {}).get("python_version"),
        data.get("require",{}).get('packages', None)
    )