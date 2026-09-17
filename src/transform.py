import pandas as pd


def transform_weather(data, latitude, longitude):
    df = pd.DataFrame(
        {
            "latitude": latitude,
            "longitude": longitude,
            "date": data["daily"]["time"],
            "temp_max": data["daily"]["temperature_2m_max"],
            "temp_min": data["daily"]["temperature_2m_min"],
            "precipitation": data["daily"]["precipitation_sum"],
            "weather_code": data["daily"]["weather_code"],
        }
    )

    df["date"] = pd.to_datetime(df["date"])

    return df
