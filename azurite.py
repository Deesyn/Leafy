import sys

"""class StdoutHook:
    def __init__(self, original, color=""):
        self.original = original
        self.color = color

    def write(self, data):
        hooked = data
        if "discord.client" in data.lower() or 'discord.gateway: Shard ID None has connected to Gateway (Session ID:' in data.lower():
            hooked = f"\033[37m[Discord.py] {data}\033[0m"  # trắng
        else:
            hooked = f"\033[37m{data}\033[0m"  # đỏ
        self.original.write(hooked)

    def flush(self):
        self.original.flush()

sys.stdout = StdoutHook(sys.stdout)  # trắng
sys.stderr = StdoutHook(sys.stderr)  # đỏ
"""
import platform
from Azurite.src.main import main

if __name__ == '__main__':
    print(f"Running on {platform.python_version()}")
    print(f"Python path {sys.executable}")
    main()
