import math
import yaml
import psutil
from functools import lru_cache

def thread_calculator(plugins_list) -> dict:
    """

    :param plugins_list:
    :return:
        {
            "total_thread": total_thread,
            "plugin_per_thread": plugin_per_thread
        }
    """
    count_plugins = len(plugins_list)
    cpu_core = psutil.cpu_count(logical=True) or 1

    if count_plugins > cpu_core:
        plugin_per_thread = math.ceil(count_plugins / cpu_core)
        total_thread = cpu_core
    else:
        plugin_per_thread = 2
        total_thread = count_plugins // 2

    return {
        "total_thread": total_thread,
        "plugin_per_thread": plugin_per_thread
    }

