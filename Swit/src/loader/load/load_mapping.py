import os
import json
from functools import lru_cache
import zipfile,rarfile
from Swit.src.handler.file.path_manager import path
from Swit.src.handler.file.extract import extract
@lru_cache(maxsize=3)
def _load_mapping(plugin_name: str, plugin_object):
    try:
        if isinstance(plugin_object, str) and (plugin_object.endswith('.zip') or plugin_object.endswith('.rar')):
            plugin_full_path = os.path.join(path.plugin(), plugin_object)

            if plugin_object.endswith('.zip'):
                archive = extract.zip(plugin_full_path)
            else:
                archive = extract.rar(plugin_full_path)

            with archive.open("mapping.json") as f:
                return json.load(f)

        elif isinstance(plugin_object, (zipfile.ZipFile, rarfile.RarFile)):
            with plugin_object.open("mapping.json") as f:
                return json.load(f)

        else:
            mapping_path = os.path.join(path.plugin(), plugin_name, "mapping.json")
            with open(mapping_path, "r", encoding="utf-8") as f:
                return json.load(f)

    except Exception as e:
        raise RuntimeError(f"Failed to load mapping.json for '{plugin_name}': {e}")