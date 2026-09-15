import string

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





class LRUcacheAside:
    def __init__(self, redis_client: redis.Redis, default_ttl: int, eviction_policy: str):
        self.redis_client = redis_client
        self.default_ttl = default_ttl
        self.eviction_policy = eviction_policy
        if self.eviction_policy == "LRU":
            self.evictionque = "lru_queue"

    async def get(self, key: str, loader, ttl) -> json:
        cached_value = self.redis_client.get(key)
        if cached_value is not None:
            await self.reload()  # Update the LRU queue to mark this key as recently used
            return cached_value
        value = await loader(key)
        if value is not None:
            self.redis_client.set(key, json.dumps(value), ex=ttl or self.default_ttl)
            await self.checkWhenFUll(key)
        return value

    async def checkWhenFUll(self, key):
        maxelements = 4
        length = self.redis_client.llen("lru_queue")
        #first checks when full if the number of elements in the queue exceeds the limit, if it does it removes the least recently used key from the queue and deletes it from redis, otherwise it adds the new key to the end of the queue
        if length > maxelements:  
            oldest_key = self.redis_client.lpop("lru_queue")  # Remove the least recently used key from the queue
            self.redis_client.lrem("lru_queue", 1, key)  # Remove the least recently used key from the queue
            self.redis_client.rpush("lru_queue", key)
            self.redis_client.delete(oldest_key)  # Delete the least recently used key from Redis
        else:
            self.redis_client.rpush("lru_queue", key)  # Add the new key to the end of the queue

    async def reload(self):
        keys = self.redis_client.keys('*')
        for key in keys:
            if not self.redis_client.exists(key):
                self.redis_client.lrem("lru_queue", 1, key)




