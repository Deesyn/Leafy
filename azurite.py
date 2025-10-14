import sys
import platform
from Moss.src.main import main
from Moss.src.utils.Local_Logger import Logger
if __name__ == '__main__':
    Logger.INFO(f"Running on {platform.python_version()}")
    Logger.INFO(f"Python path {sys.executable}")
    main()
