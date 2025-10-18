import os
import json
from functools import lru_cache
import zipfile,rarfile
from Swit.src.utils.file_handler.path_manager import path
from Swit.src.utils.file_handler.extract import extract
@lru_cache(maxsize=3)
def _load_mapping(plugin_name: str, plugin_source):
    try:
        if isinstance(plugin_source, str) and (plugin_source.endswith('.zip') or plugin_source.endswith('.rar')):
            plugin_full_path = os.path.join(path.plugin(), plugin_source)

            if plugin_source.endswith('.zip'):
                archive = extract.zip(plugin_full_path)
            else:
                archive = extract.rar(plugin_full_path)

            with archive.open("mapping.json") as f:
                return json.load(f)

        elif isinstance(plugin_source, (zipfile.ZipFile, rarfile.RarFile)):
            with plugin_source.open("mapping.json") as f:
                return json.load(f)

        else:
            mapping_path = os.path.join(path.plugin(), plugin_name, "mapping.json")
            with open(mapping_path, "r", encoding="utf-8") as f:
                return json.load(f)

    except Exception as e:
        raise RuntimeError(f"Failed to load mapping.json for '{plugin_name}': {e}")