import psutil


def thread_calculator(plugins_list) -> dict:
    count_plugins = len(plugins_list)

    even = False
    odd = False

    cpu_core = psutil.cpu_count(logical=True) + psutil.cpu_count(logical=False)

    if cpu_core % 2 == 0 and count_plugins % 2 == 0:
        even = True
    else:
        odd = True

    if even:
        for pl in plugins_list:
            pass