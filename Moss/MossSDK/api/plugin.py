class plugin():
    total_plugin = None
    @classmethod
    def plugin_init(cls,total_plugin,plugin_list):
        cls.total_plugin = total_plugin
        cls.plugin_list = plugin_list

    @staticmethod
    def get_total_plugin(cls) -> int:
        """
        Returns the total number of plugins that loaded successfully and those that failed.

        Returns:
            int: total number of plugins
        """
        if cls.total_plugin is None:
            return 0
        return cls.total_plugin

    @staticmethod
    def get_plugin_list_success(cls):
        if cls.plugin_list is None:
            return []
        return cls.plugin_list
    @staticmethod
    def get_plugin_list_failed(cls):
        pass
    @staticmethod
    def get_plugin_list(cls):
        pass
