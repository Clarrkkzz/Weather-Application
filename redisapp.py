import redis
from requests import get
import json

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

class fifofull:
    async def pstorage():
        maxsize_mb = 100 
        maxsize = maxsize_mb * 1024 * 1024  # Convert MB to bytesmaxsize = maxsize_mb * 1024 * 1024  # Convert MB to bytes
        info = redis_client.info()
        used = info['used_memory']
        if used > maxsize:  # If Redis memory usage exceeds the specified size
            oldest_key = redis_client.lpop("fifo_queue") # Clear the cache
            redis_client.delete(oldest_key)  # Delete the oldest key from Redis
    async def noofelement():
        maxelements = 4 
        length = redis_client.llen("fifo_queue")
        if length > maxelements:  # If Redis memory usage exceeds the specified size
            oldest_key = redis_client.lpop("fifo_queue") # Clear the cache
            redis_client.delete(oldest_key)  # Delete the oldest key from Redis


class cacheAside:
    def __init__(self, redis_client: redis.Redis, default_ttl: int = 3600):
        self.redis_client = redis_client
        self.default_ttl = default_ttl

    async def get(self, key: str, loader, ttl):
        cached_value = self.redis_client.get(key)
        if cached_value is not None:
            return cached_value
        value = await loader(key)
        if value is not None:
            self.redis_client.set(key, json.dumps(value), ex=ttl or self.default_ttl)
        return value

