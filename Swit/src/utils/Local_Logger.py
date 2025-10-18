from datetime import datetime
from rich.console import Console

console = Console()

class Logger:
    COLORS = {
        "INFO": "rgb(100,255,100)",
        "SUCCESS": "rgb(0,255,180)",
        "LOAD": "rgb(255,255,100)",
        "WARN": "rgb(255,215,0)",
        "ERROR": "rgb(255,90,90)",
        "CRITICAL": "bold rgb(255,0,200)",
        "DEBUG": "rgb(120,170,255)",
        "LOADER": "rgb(190,120,255)"
    }

    @staticmethod
    def _log(level: str, color: str, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        console.print(
            f"[rgb(130,129,129)][{timestamp}][/rgb(130,129,129)] "
            f"[{color}][Swit/{level}][/{color}] "
            f"[white]{message}[/white]"
        )

    @staticmethod
    def INFO(message: str): Logger._log("INFO", Logger.COLORS["INFO"], message)
    @staticmethod
    def SUCCESS(message: str): Logger._log("SUCCESS", Logger.COLORS["SUCCESS"], message)
    @staticmethod
    def LOAD(message: str): Logger._log("LOAD", Logger.COLORS["LOAD"], message)
    @staticmethod
    def WARN(message: str): Logger._log("WARN", Logger.COLORS["WARN"], message)
    @staticmethod
    def ERROR(message: str): Logger._log("ERROR", Logger.COLORS["ERROR"], message)
    @staticmethod
    def DEBUG(message: str, debug: bool = False):
        if debug: Logger._log("DEBUG", Logger.COLORS["DEBUG"], message)
    @staticmethod
    def CRITICAL(message: str): Logger._log("CRITICAL", Logger.COLORS["CRITICAL"], message)
    @staticmethod
    def LOADER(message: str): Logger._log("LOADER", Logger.COLORS["LOADER"], message)
