

import json
import os
import httpx


async def fetch_weather_from_api(base_url, location, start_date, end_date) -> json: 
            API_KEY = os.getenv("VISUAL_CROSSING_API_KEY")
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
                    return json.dumps(data)

