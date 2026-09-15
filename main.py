import os
from fastapi import FastAPI, Request
from dotenv import load_dotenv
import httpx
import redis 
from token_bucket import TokenBucket
from repositories.redisapp import fifofull, LRUcacheAside 
import json
from api.weather import fetch_weather_from_api


load_dotenv()

app = FastAPI()


redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

API_KEY = os.getenv("VISUAL_CROSSING_API_KEY")
base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
cache = LRUcacheAside(redis_client=redis_client, default_ttl=3600, eviction_policy="LRU")

limiter = TokenBucket(
    redis_client=redis_client,
    capacity=10,        # Maximum burst size
    refill_rate=1,      # Add 1 token per interval
    refill_interval=1.0 # Every 1 second
)



cache = LRUcacheAside(redis_client=redis.Redis(host='localhost', port=6379, decode_responses=True), default_ttl=3600, eviction_policy="LRU")

async def cache_eviction(key):
    await cache.checkWhenFUll(key) #checks if the number of elements doesnt exceed a certain amount set 
    await cache.reload() #checks any expired keys and updated queue

@app.get("/")
async def root():
    return {"message": "Welcome to the Weather API"}



@app.get("/weather/{location}/{start_date}/{end_date}")
async def get_weather(request: Request, location: str, start_date: str, end_date: str):
    try:
        cache_key = f"{location}_{start_date}_{end_date}"
        #loader function to get the data from the API if not presentin  cache
        #loads the data from cache is present, otherwise calls the loader function defined earlier to get the data from the API  
        client_ip = request.client.host
        allowed, remaining = limiter.allow(f"ip:{client_ip}")
        if not allowed:
            return {"error": "Rate limit exceeded. Please try again later."}, 429
            
        data = await cache.get(cache_key, loader=lambda _: fetch_weather_from_api(base_url, location, start_date, end_date), ttl=3600)

        #if data is not None, add the key to the LRU queue and call the noof element function to check if the number of elements in the queue exceeds the limit 
        if data is not None:
            await cache_eviction(cache_key)  # Check and manage cache eviction if necessary
            return data  

        return {
            "error"
        }, 502
    
    except Exception as e:
        return {"error": str(e)}, 500
    
        


