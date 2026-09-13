import os
from fastapi import FastAPI
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("VISUAL_CROSSING_API_KEY")
base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

response = requests.get(f"{base_url}/New York?unitGroup=metric&key={API_KEY}&contentType=json")

print(response.json())