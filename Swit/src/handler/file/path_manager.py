from pathlib import Path

class path():
    @staticmethod
    def plugin_extract(plugin_name):
        return (Path(__file__).parent.parent.parent.parent.parent / 'cache' / 'plugin_extract' / plugin_name)
    @staticmethod
    def root():
        return (Path(__file__).parent.parent.parent.parent.parent)
    @staticmethod
    def config():
        return (Path(__file__).parent.parent.parent.parent.parent / "swit.yml").resolve()
    @staticmethod
    def plugin():
        return (Path(__file__).parent.parent.parent.parent.parent / "plugins")