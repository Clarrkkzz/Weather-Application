import os
from fastapi import FastAPI
from dotenv import load_dotenv
import httpx
import redis 

load_dotenv()

app = FastAPI()

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)


@app.get("/")
async def root():
    return {"message": "Welcome to the Weather API"}

@app.get("/weather/{location}/{start_date}/{end_date}")
async def get_weather(location: str, start_date: str, end_date: str):
    try:
        async with httpx.AsyncClient() as client:
                cache_key = f"{location}_{start_date}_{end_date}"
                if redis_client.exists(cache_key):
                    cached_data = redis_client.get(cache_key)
                    return {"data": cached_data, "source": "cache"}

                response = await client.get(f"{base_url}/{location}/{start_date}/{end_date}?unitGroup=metric&key={API_KEY}&contentType=json")
                if response.status_code == 200:
                    data = response.json()
                    redis_client.set(cache_key, str(data))  # Cache for 1 hour
                    return data
                else:
                    return {"error": "Unable to fetch weather data", "status_code": response.status_code}
    except Exception as e:
        return {"error": str(e)}
    
        
    

API_KEY = os.getenv("VISUAL_CROSSING_API_KEY")
base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
