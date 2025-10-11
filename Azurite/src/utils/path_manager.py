from pathlib import Path

class path():
    @staticmethod
    def config():
        return (Path(__file__).parent.parent.parent.parent / "azurite.yml").resolve()
    @staticmethod
    def plugin():
        return (Path(__file__).parent.parent.parent.parent / "plugins")