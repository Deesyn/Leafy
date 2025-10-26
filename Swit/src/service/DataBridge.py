from dataclasses import dataclass
import random
import threading
from typing import Dict, Optional
from functools import lru_cache

@dataclass
class PluginData:
    plugin_name: str
    plugin_id: int

class DataBridge:
    _store: Dict[str, PluginData] = {}
    _lock = threading.Lock()
    @classmethod
    def add_id(cls, plugin_name: str) -> int:
        """Add a plugin id if missing, return the plugin_id (existing or new)."""
        with cls._lock:
            existing = cls._store.get(plugin_name)
            if existing is not None:
                return existing.plugin_id

            plugin_id = random.randint(1_000_000_000, 9_999_999_999)
            pd = PluginData(plugin_name=plugin_name, plugin_id=plugin_id)
            cls._store[plugin_name] = pd
            return plugin_id

    @classmethod
    def get_id(cls, plugin_name: str) -> Optional[int]:
        """Return plugin_id or None if not found."""
        pd = cls._store.get(plugin_name)
        return pd.plugin_id if pd else None
