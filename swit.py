import sys
import platform
from Swit.src.core.main import main
from Swit.src.utils.Logger import Logger
if __name__ == '__main__':
    Logger.INFO(f"Running on {platform.python_version()}")
    Logger.INFO(f"Python path {sys.executable}")
    main()
