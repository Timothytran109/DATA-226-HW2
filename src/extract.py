import requests


def extract_weather(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "past_days": 60,
        "forecast_days": 0,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "weather_code",
        ],
        "timezone": "Asia/Tokyo",
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json()
