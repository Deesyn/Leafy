import math
import psutil
from functools import lru_cache

@lru_cache(maxsize=3)
def thread_calculator(plugins_list) -> dict:
    count_plugins = len(plugins_list)
    cpu_core = psutil.cpu_count(logical=True) or 1

    if count_plugins > cpu_core:
        plugin_per_thread = math.ceil(count_plugins / cpu_core)
        total_thread = cpu_core
    else:
        plugin_per_thread = 1
        total_thread = count_plugins

    return {
        "total_thread": total_thread,
        "plugin_per_thread": plugin_per_thread
    }
