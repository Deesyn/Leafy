from colorama import Fore

class Logger():
    base_logger = None
    @classmethod
    def _set_base(cls,logger):
        cls.base_logger = logger
