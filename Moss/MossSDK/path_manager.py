from pathlib import Path

class path():
    @staticmethod
    def config() -> Path:
        """
        EN:
            Returns the exact path of the azurite config folder
        VI:
            Trả về path chính xác của folder config của azurite
        :return: Moss config path
        """
        return (Path(__file__).parent.parent.parent / "config").resolve()
