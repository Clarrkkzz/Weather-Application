import httpx

cities = [
    "Tehran",
    "Manila",
    "Beijing",
    "Washington",
    "London"
]

for city in cities:
    result = httpx.get(
        f"http://127.0.0.1:8000/weather/{city}/2026-10-02/2026-10-04"
    )

    print(city, result.status_code)
    print(result.json())