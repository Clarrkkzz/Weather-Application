import os
from fastapi import FastAPI
from dotenv import load_dotenv
import httpx

load_dotenv()

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to the Weather API"}

@app.get("/weather/{location}/{start_date}/{end_date}")
async def get_weather(location: str, start_date: str, end_date: str):
    try:
        async with httpx.AsyncClient() as client:
                response = await client.get(f"{base_url}/{location}/{start_date}/{end_date}?unitGroup=metric&key={API_KEY}&contentType=json")
                if response.status_code == 200:
                    return response.json()
                else:
                    return {"error": "Unable to fetch weather data", "status_code": response.status_code}
    except Exception as e:
        return {"error": str(e)}
    
        
    

API_KEY = os.getenv("VISUAL_CROSSING_API_KEY")
base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
