"""Caching utilities for EduChat."""

from typing import Dict, Optional, Any
from datetime import datetime, timedelta
import hashlib
import json


class SimpleCache:
    """Simple in-memory cache with TTL support."""
    
    def __init__(self, default_ttl: int = 3600):
        """Initialize cache.
        
        Args:
            default_ttl: Default time-to-live in seconds (default: 1 hour)
        """
        self._cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = default_ttl
        self.hits = 0
        self.misses = 0
    
    def _generate_key(self, data: Any) -> str:
        """Generate cache key from data.
        
        Args:
            data: Data to generate key from
        
        Returns:
            Cache key string
        """
        # Convert to JSON and hash
        json_str = json.dumps(data, sort_keys=True)
        return hashlib.md5(json_str.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache.
        
        Args:
            key: Cache key
        
        Returns:
            Cached value or None if not found/expired
        """
        if key not in self._cache:
            self.misses += 1
            return None
        
        entry = self._cache[key]
        
        # Check if expired
        if datetime.now() > entry["expires_at"]:
            del self._cache[key]
            self.misses += 1
            return None
        
        self.hits += 1
        return entry["value"]
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (optional)
        """
        expires_at = datetime.now() + timedelta(seconds=ttl or self.default_ttl)
        
        self._cache[key] = {
            "value": value,
            "expires_at": expires_at,
            "created_at": datetime.now(),
        }
    
    def delete(self, key: str):
        """Delete value from cache.
        
        Args:
            key: Cache key
        """
        if key in self._cache:
            del self._cache[key]
    
    def clear(self):
        """Clear all cached values."""
        self._cache.clear()
        self.hits = 0
        self.misses = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics.
        
        Returns:
            Dictionary with cache stats
        """
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "size": len(self._cache),
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": round(hit_rate, 2),
            "total_requests": total_requests,
        }
    
    def cleanup_expired(self):
        """Remove expired entries from cache."""
        now = datetime.now()
        expired_keys = [
            key for key, entry in self._cache.items()
            if now > entry["expires_at"]
        ]
        
        for key in expired_keys:
            del self._cache[key]
        
        return len(expired_keys)


# Global cache instances
_response_cache: Optional[SimpleCache] = None
_data_cache: Optional[SimpleCache] = None


def get_response_cache() -> SimpleCache:
    """Get global response cache instance.
    
    Returns:
        SimpleCache for AI responses (1 hour TTL)
    """
    global _response_cache
    if _response_cache is None:
        _response_cache = SimpleCache(default_ttl=3600)  # 1 hour
    return _response_cache


def get_data_cache() -> SimpleCache:
    """Get global data cache instance.
    
    Returns:
        SimpleCache for institution data (24 hour TTL)
    """
    global _data_cache
    if _data_cache is None:
        _data_cache = SimpleCache(default_ttl=86400)  # 24 hours
    return _data_cache


def cache_response(func):
    """Decorator to cache function responses.
    
    Args:
        func: Function to cache
    
    Returns:
        Wrapped function with caching
    """
    async def async_wrapper(*args, **kwargs):
        cache = get_response_cache()
        
        # Generate cache key from args
        cache_key = cache._generate_key({
            "func": func.__name__,
            "args": args,
            "kwargs": kwargs,
        })
        
        # Check cache
        cached_value = cache.get(cache_key)
        if cached_value is not None:
            return cached_value
        
        # Call function and cache result
        result = await func(*args, **kwargs)
        cache.set(cache_key, result)
        
        return result
    
    def sync_wrapper(*args, **kwargs):
        cache = get_response_cache()
        
        # Generate cache key from args
        cache_key = cache._generate_key({
            "func": func.__name__,
            "args": args,
            "kwargs": kwargs,
        })
        
        # Check cache
        cached_value = cache.get(cache_key)
        if cached_value is not None:
            return cached_value
        
        # Call function and cache result
        result = func(*args, **kwargs)
        cache.set(cache_key, result)
        
        return result
    
    # Return appropriate wrapper based on function type
    import asyncio
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper
