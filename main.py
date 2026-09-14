import os
from fastapi import FastAPI, Request
from dotenv import load_dotenv
import httpx
import redis 
from token_bucket import TokenBucket
from redisapp import fifofull, cacheAside


load_dotenv()

app = FastAPI()

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

limiter = TokenBucket(
    redis_client=redis_client,
    capacity=10,        # Maximum burst size
    refill_rate=1,      # Add 1 token per interval
    refill_interval=1.0 # Every 1 second
)



@app.get("/")
async def root():
    return {"message": "Welcome to the Weather API"}

@app.get("/weather/{location}/{start_date}/{end_date}")
async def get_weather(request: Request, location: str, start_date: str, end_date: str):
    try:
        cache_key = f"{location}_{start_date}_{end_date}"
        #loader function to get the data from the API if not presentin  cache
        async def fetch_weather_from_api(key=None):
            async with httpx.AsyncClient() as client:
                url = f"{base_url}/{location}/{start_date}/{end_date}?unitGroup=metric&key={API_KEY}&contentType=json"
                params = {
                    "unitGroup": "metric",
                    "key": API_KEY,
                    "contentType": "json"
                }
                response = await client.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    return data
        #loads the data from cache is present, otherwise calls the loader function defined earlier to get the data from the API  
        client_ip = request.client.host
        allowed = limiter.allow(f"ip:{client_ip}")
        if not allowed:
            return {"error": "Rate limit exceeded. Please try again later."}, 429
            
        data = await cacheAside(redis_client).get(cache_key, loader=fetch_weather_from_api, ttl=3600)


        #if data is not None, add the key to the fifo queue and call the noof element function to check if the number of elements in the queue exceeds the limit 
        if data is not None:
            redis_client.lpush("fifo_queue", cache_key)  # Add the key to the FIFO queue
            await fifofull.noofelement()
            return data  

        return {
            "error"
        }, 502
    
    except Exception as e:
        return {"error": str(e)}, 500
    
        


API_KEY = os.getenv("VISUAL_CROSSING_API_KEY")
base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
