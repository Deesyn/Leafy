import sys
import platform
from Azurite.src.main import main

if __name__ == '__main__':
    print(f"Running on {platform.python_version()}")
    print(f"Python path {sys.executable}")
    main()
