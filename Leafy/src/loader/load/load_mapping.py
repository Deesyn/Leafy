import os
import json
from functools import lru_cache
from Leafy.src.utils.file_handler.path_manager import path
@lru_cache(maxsize=3)
def _load_mapping(plugin_name: str, plugin_source):
    try:
        if hasattr(plugin_source, "open"):
            with plugin_source.open("mapping.json") as f:
                return json.load(f)
        mapping_path = os.path.join(path.plugin(), plugin_name, "mapping.json")
        with open(mapping_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except Exception as e:
        raise RuntimeError(f"Failed to load mapping.json for '{plugin_name}': {e}")