import subprocess
import sys
from Leafy.src.utils.Local_Logger import Logger
from Leafy.src.utils.cache_handler.cache import Cache

def download_package(package_list):
    cache_file_name = 'package_download_cache'
    Cache.create(file=cache_file_name)
    Cache_file_data = str(Cache.read(file=cache_file_name)).split('\n')

    for package in package_list:
        if package in Cache_file_data:
            continue
        Logger.LOADER(f'Download package: {package}')
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', package],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        Logger.SUCCESS(f"Download {package} success!")
        Cache.write(file=cache_file_name, data=f"{package}\n", append=True)

download_package(['discord.py', 'colorama'])
