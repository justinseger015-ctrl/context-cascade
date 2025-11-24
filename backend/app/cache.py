# Simple in-memory cache for performance optimization
# Used to cache frequently accessed data (agents, permissions)

from datetime import datetime, timedelta
from typing import Any, Optional, Dict
import json

class SimpleCache:
    """Simple thread-safe in-memory cache with TTL"""

    def __init__(self):
        self._cache: Dict[str, tuple[Any, datetime]] = {}
        self._default_ttl = timedelta(minutes=5)

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired"""
        if key in self._cache:
            value, expires_at = self._cache[key]
            if datetime.utcnow() < expires_at:
                return value
            else:
                # Expired, remove from cache
                del self._cache[key]
        return None

    def set(self, key: str, value: Any, ttl: Optional[timedelta] = None):
        """Set value in cache with TTL"""
        if ttl is None:
            ttl = self._default_ttl
        expires_at = datetime.utcnow() + ttl
        self._cache[key] = (value, expires_at)

    def delete(self, key: str):
        """Delete key from cache"""
        if key in self._cache:
            del self._cache[key]

    def clear(self):
        """Clear all cache entries"""
        self._cache.clear()

    def size(self) -> int:
        """Get number of cached items"""
        # Clean expired entries first
        now = datetime.utcnow()
        expired_keys = [k for k, (_, exp) in self._cache.items() if exp < now]
        for k in expired_keys:
            del self._cache[k]
        return len(self._cache)

# Global cache instance
cache = SimpleCache()
