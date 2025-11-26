import os
import asyncio
try:
    import redis.asyncio as aioredis
except Exception:
    aioredis = None

class InMemoryCache:
    def __init__(self):
        self.store = {}

    async def get(self, key):
        v = self.store.get(key)
        if not v:
            return None
        value, expires = v
        if expires and expires < asyncio.get_event_loop().time():
            del self.store[key]
            return None
        return value

    async def set(self, key, value, ttl=None):
        expires = None
        if ttl:
            expires = asyncio.get_event_loop().time() + ttl
        self.store[key] = (value, expires)


class RedisCache:
    def __init__(self, host, password=None):
        self.client = aioredis.from_url(f"redis://{host}", password=password, decode_responses=True)

    async def get(self, key):
        return await self.client.get(key)

    async def set(self, key, value, ttl=None):
        if ttl:
            await self.client.set(key, value, ex=ttl)
        else:
            await self.client.set(key, value)


_cache = None

def get_cache():
    global _cache
    if _cache:
        return _cache
    host = os.getenv('CACHE_HOST')
    pwd = os.getenv('CACHE_PASSWORD')
    if host and aioredis:
        _cache = RedisCache(host, password=pwd)
    else:
        _cache = InMemoryCache()
    return _cache
