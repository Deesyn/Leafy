from pathlib import Path

class path():
    @staticmethod
    def root():
        return (Path(__file__).parent.parent.parent.parent.parent)
    @staticmethod
    def config():
        return (Path(__file__).parent.parent.parent.parent.parent / "swit.yml").resolve()
    @staticmethod
    def plugin():
        return (Path(__file__).parent.parent.parent.parent.parent / "plugins")