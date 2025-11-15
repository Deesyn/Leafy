import os
from pathlib import Path

from Swit.src.utils.Logger import Logger


class Cache:
    cache_dir = Path(__file__).resolve().parent.parent.parent.parent / "cache"

    @staticmethod
    def _ensure_dir() -> None:
        Cache.cache_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def create(file: str) -> Path:
        Cache._ensure_dir()
        cache_file = Cache.cache_dir / file
        cache_file.touch(exist_ok=True)

        return cache_file



    @staticmethod
    def read(file: str) -> str:
        Cache._ensure_dir()
        path = Cache.cache_dir / file
        if not path.exists():
            return "cache path not exists"
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = f.read()
                Logger.DEBUG(f"Found {len(data)} bytes from {file}")
                Logger.DEBUG(f"Read at: {path}")
                return data
        except Exception as e:
            return f"error reading cache: {e}"

    @staticmethod
    def write(file: str, data: str, append: bool = False) -> None:
        Cache._ensure_dir()
        mode = "a" if append else "w"
        try:
            with open(Cache.cache_dir / file, mode, encoding="utf-8") as f:
                Logger.DEBUG(f"Write cache: {data}")
                f.write(data)
                Logger.DEBUG(f"Write at: {Cache.cache_dir / file}")
                Logger.DEBUG('Write cache success!')
        except Exception as e:
            Logger.ERROR(f"Error writing cache: {e}")

    @staticmethod
    def delete(file: str) -> bool:
        Cache._ensure_dir()
        path = Cache.cache_dir / file
        if path.exists():
            path.unlink()
            return True
        return False

    @staticmethod
    def clear() -> None:
        Cache._ensure_dir()
        for f in Cache.cache_dir.iterdir():
            if f.is_file():
                f.unlink()

    @staticmethod
    def list() -> list[str]:
        Cache._ensure_dir()
        return [f.name for f in Cache.cache_dir.iterdir() if f.is_file()]
