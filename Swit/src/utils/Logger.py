import os.path
from datetime import datetime
from rich.console import Console
from Swit.src.handler.file.config import Config
from Swit.src.handler.file.path_manager import path
from Swit.src.utils.StatusCode import StatusCode
console = Console()

log_path = None

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
    def createLog():

        global log_path
        if log_path:
            return
        log_path = os.path.join(
            path.root(),
            'logs',
            f"Swit-log-{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.log"
        )

        with open(log_path, 'w', encoding='utf-8') as f:
            f.write(f"write log at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        return log_path

    @staticmethod
    def getLogPath():
        if log_path:
            return log_path
        else:
            return StatusCode.NOT_FOUND


    @staticmethod
    def _log(level: str, color: str, message: str):
        Logger.createLog()
        global log_path
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if log_path:
            with open(log_path, 'a', encoding='utf-8') as f:
                f.writelines(f"[{timestamp}] [Swit/{level}] > {message}\n")

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
    def CRITICAL(message: str): Logger._log("CRITICAL", Logger.COLORS["CRITICAL"], message)
    @staticmethod
    def LOADER(message: str): Logger._log("LOADER", Logger.COLORS["LOADER"], message)
    @staticmethod
    def DEBUG(message:str ):
        if Config.Other.debug():
            Logger._log('DEBUG', Logger.COLORS['DEBUG'], message)
