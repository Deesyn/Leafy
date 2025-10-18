from Swit.src.utils.Local_Logger import Logger
def print_plugin_dir_tree(plugin_list):
    for i, plugin in enumerate(plugin_list):
        if i < len(plugin_list) - 1:
            Logger.INFO(f"├── {plugin}")
        else:
            Logger.INFO(f"└── {plugin}")