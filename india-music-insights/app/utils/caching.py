"""
Simple in-memory TTL cache for API responses
"""

import asyncio
import time
from typing import Any, Optional, Dict, Callable
from dataclasses import dataclass
import json
import hashlib


@dataclass
class CacheItem:
    """Cache item with expiration"""
    data: Any
    expires_at: float
    
    @property
    def is_expired(self) -> bool:
        return time.time() > self.expires_at


class TTLCache:
    """
    Simple in-memory TTL (Time To Live) cache
    """
    
    def __init__(self, default_ttl: int = 300):
        """
        Initialize cache
        
        Args:
            default_ttl: Default TTL in seconds (300 = 5 minutes)
        """
        self.default_ttl = default_ttl
        self._cache: Dict[str, CacheItem] = {}
        self._lock = asyncio.Lock()
    
    def _generate_key(self, prefix: str, **kwargs) -> str:
        """
        Generate cache key from prefix and kwargs
        
        Args:
            prefix: Key prefix
            **kwargs: Key parameters
            
        Returns:
            str: Generated cache key
        """
        # Create deterministic key from kwargs
        key_data = json.dumps(kwargs, sort_keys=True)
        key_hash = hashlib.md5(key_data.encode()).hexdigest()[:8]
        return f"{prefix}:{key_hash}"
    
    async def get(self, key: str) -> Optional[Any]:
        """
        Get item from cache
        
        Args:
            key: Cache key
            
        Returns:
            Cached data or None if not found/expired
        """
        async with self._lock:
            item = self._cache.get(key)
            
            if item is None:
                return None
            
            if item.is_expired:
                del self._cache[key]
                return None
            
            return item.data
    
    async def set(self, key: str, data: Any, ttl: Optional[int] = None) -> None:
        """
        Set item in cache
        
        Args:
            key: Cache key
            data: Data to cache
            ttl: TTL in seconds (uses default if None)
        """
        ttl = ttl or self.default_ttl
        expires_at = time.time() + ttl
        
        async with self._lock:
            self._cache[key] = CacheItem(data=data, expires_at=expires_at)
    
    async def delete(self, key: str) -> bool:
        """
        Delete item from cache
        
        Args:
            key: Cache key
            
        Returns:
            bool: True if item was deleted, False if not found
        """
        async with self._lock:
            return self._cache.pop(key, None) is not None
    
    async def clear(self) -> None:
        """Clear all items from cache"""
        async with self._lock:
            self._cache.clear()
    
    async def cleanup_expired(self) -> int:
        """
        Remove expired items from cache
        
        Returns:
            int: Number of items removed
        """
        current_time = time.time()
        expired_keys = []
        
        async with self._lock:
            for key, item in self._cache.items():
                if item.expires_at <= current_time:
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self._cache[key]
        
        return len(expired_keys)
    
    def size(self) -> int:
        """Get current cache size"""
        return len(self._cache)
    
    def cache_key(self, prefix: str, **kwargs) -> str:
        """Generate cache key (convenience method)"""
        return self._generate_key(prefix, **kwargs)


def cached(
    cache: TTLCache, 
    key_prefix: str, 
    ttl: Optional[int] = None,
    key_func: Optional[Callable[..., str]] = None
):
    """
    Decorator for caching async function results
    
    Args:
        cache: TTLCache instance
        key_prefix: Prefix for cache keys
        ttl: TTL in seconds
        key_func: Custom function to generate cache key from args
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                # Use function name and arguments
                cache_key = cache._generate_key(
                    f"{key_prefix}:{func.__name__}",
                    args=str(args),
                    kwargs=kwargs
                )
            
            # Try to get from cache
            cached_result = await cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            await cache.set(cache_key, result, ttl)
            
            return result
        
        return wrapper
    return decorator


# Global cache instance
cache = TTLCache(default_ttl=300)  # 5 minutes default
