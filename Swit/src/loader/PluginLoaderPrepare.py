# MIT License
# Copyright (c) 2025 kenftr


def prepare(plugin_path, plugin_name: str):

    from Swit.src.loader.load.LoadMapping import _load_mapping
    from Swit.src.handler.file.config import Config
    from Swit.src.utils.logger import Logger
    from Swit.src.loader.utils.CheckPythonVersion import _check_python_version

    if plugin_path:
        mapping_data = _load_mapping(plugin_path=plugin_path, plugin_ref=plugin_name, plugin_object=None)
    else:
        mapping_data = _load_mapping(plugin_path=None, plugin_ref=plugin_name, plugin_object=None)
    mapping_config = Config.Mapping()
    if mapping_config.get('format', 'Swit-mapping-v2') != mapping_data['mapping']['format']:
        Logger.LOADER(
            f"Plugin {plugin_name} uses {mapping_data['mapping']['format']} format instead of required {mapping_config['format']}. Skipping...")
        return
    if not _check_python_version(plugin_path=plugin_path, plugin_ref=plugin_name):
        Logger.WARN(f"Skipped {plugin_name} (Python version incompatible)")
        return