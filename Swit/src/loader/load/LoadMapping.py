import os
import json
from functools import lru_cache
import zipfile,rarfile
from Swit.src.handler.file.path_manager import path
from Swit.src.handler.file.extract import extract
@lru_cache(maxsize=3)
def _load_mapping(plugin_path: None,plugin_ref: str, plugin_object: None):
    try:
        if plugin_object:
            plugin_name = plugin_ref
            plugin_ref = plugin_object
        if plugin_path:
            try:
                if os.path.exists(os.path.join(str(plugin_path))):
                    with open(os.path.join(str(plugin_path),'mapping.json'),'r',encoding='utf-8') as f:
                        return json.load(f)
                else:
                    return None
            except Exception as e:
                raise e

        if isinstance(plugin_ref, str) and (plugin_ref.endswith('.zip') or plugin_ref.endswith('.rar')):
            plugin_full_path = os.path.join(path.plugin_extract(plugin_ref))

            if plugin_ref.endswith('.zip'):
                archive = extract.zip(plugin_full_path)
            else:
                archive = extract.rar(plugin_full_path)

            with archive.open("mapping.json") as f:
                return json.load(f)

        elif isinstance(plugin_ref, (zipfile.ZipFile, rarfile.RarFile)):
            with plugin_ref.open("mapping.json") as f:
                return json.load(f)

        else:
            mapping_path = os.path.join(path.plugin(), plugin_name if plugin_object else plugin_ref, "mapping.json")
            with open(mapping_path, "r", encoding="utf-8") as f:
                return json.load(f)

    except Exception as e:
        raise RuntimeError(f"Failed to load mapping.json for '{plugin_name if plugin_object else plugin_ref}': {e}")