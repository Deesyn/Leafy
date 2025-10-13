import sys
import inspect
from colorama import Fore

class Logger():
    base_logger = None
    @staticmethod
    def _get_caller_file():
        frame = inspect.stack()[1]
        caller_file = frame.filename
        caller_path = caller_file.split("\\")
        for i,dir in enumerate(caller_path):
            if dir.lower() == 'plugins':
                return caller_path[i+1]
