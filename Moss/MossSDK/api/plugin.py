class plugin():
    total_plugin = 0
    @classmethod
    def plugin_init(cls,total_plugin,plugin_list):
        cls.total_plugin = total_plugin
        cls.plugin_list = plugin_list

    @staticmethod
    def get_total_plugin(cls):
        return cls.total_plugin

    @staticmethod
    def get_plugin_list(cls):
        return cls.plugin_list
