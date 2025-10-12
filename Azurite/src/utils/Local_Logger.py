# Local_Logger.py
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

class Logger:

    @staticmethod
    def _log(level: str, color: str, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{color}[{Fore.WHITE}{timestamp}{color}] [{Fore.BLUE}Azurite{Fore.WHITE}/{color}{level}] {Style.RESET_ALL}{message}")

    @staticmethod
    def INFO(message: str):
        Logger._log("INFO", Fore.LIGHTGREEN_EX, message)

    @staticmethod
    def SUCCESS(message: str):
        Logger._log("SUCCESS", Fore.GREEN, message)

    @staticmethod
    def LOAD(message: str):
        Logger._log("LOADING", Fore.YELLOW, message)

    @staticmethod
    def LOADER(message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}[{timestamp}] [LOADER]{Style.RESET_ALL} {message}")

    @staticmethod
    def WARN(message: str):
        Logger._log("WARN", Fore.YELLOW, message)

    @staticmethod
    def ERROR(message: str):
        Logger._log("ERROR", Fore.RED, message)

    @staticmethod
    def DEBUG(message: str, debug: bool = False):
        if debug:
            Logger._log("DEBUG", Fore.CYAN, message)

    @staticmethod
    def CRITICAL(message: str):
        Logger._log("CRITICAL", Fore.MAGENTA + Style.BRIGHT, message)
