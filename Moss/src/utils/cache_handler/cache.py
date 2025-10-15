import os
from pathlib import Path

from Moss.src.utils.Local_Logger import Logger


class Cache:
    cache_dir = Path(__file__).resolve().parent.parent.parent.parent.parent / "cache"

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
                return f.read()
        except Exception as e:
            return f"error reading cache: {e}"

    @staticmethod
    def write(file: str, data: str, append: bool = False) -> None:
        Cache._ensure_dir()
        mode = "a" if append else "w"
        try:
            with open(Cache.cache_dir / file, mode, encoding="utf-8") as f:
                f.write(data)
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
