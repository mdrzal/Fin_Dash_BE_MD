import threading
import time
from typing import Any, Optional

class InMemoryCache:
    def __init__(self):
        self._cache = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            entry = self._cache.get(key)
            if entry:
                value, expires_at = entry
                if expires_at is None or expires_at > time.time():
                    return value
                else:
                    # Expired
                    del self._cache[key]
            return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        with self._lock:
            expires_at = time.time() + ttl if ttl else None
            self._cache[key] = (value, expires_at)

# Singleton instance
cache = InMemoryCache()

def get_cache(key: str):
    return cache.get(key)

def set_cache(key: str, value: Any, ttl: Optional[int] = 600):
    cache.set(key, value, ttl)
