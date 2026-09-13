import redis

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
        info = redis_client.info()
        length = redis_client.llen("fifo_queue")
        if length > maxelements:  # If Redis memory usage exceeds the specified size
            oldest_key = redis_client.lpop("fifo_queue") # Clear the cache
            redis_client.delete(oldest_key)  # Delete the oldest key from Redis



      


