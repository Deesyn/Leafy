# MIT License
# Copyright (c) 2025 kenftr


async def package_installer(plugin_name):
    import time
    from Swit.src.loader.handler.download_package import download_package
    from Swit.src.loader.utils.GetPluginInfo import _get_plugin_info
    _,_,_,packages_list = _get_plugin_info(plugin_path=None,plugin_name=plugin_name,plugin_object=plugin_name)
    start_time = time.time()
    download_package(package_list=packages_list)
    return round(time.time() - start_time, 4)