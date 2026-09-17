from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd
from airflow import DAG
from airflow.decorators import task
from airflow.models import Variable

from src.extract import extract_weather
from src.load import load_weather_data
from src.transform import transform_weather
from src.validate import get_record_count


@task
def extract_task(latitude, longitude):
    return extract_weather(latitude, longitude)


@task
def transform_task(data, latitude, longitude):
    df = transform_weather(
        data,
        latitude,
        longitude,
    )

    return df.to_dict(orient="records")


@task
def load_task(records):
    df = pd.DataFrame(records)

    df["date"] = pd.to_datetime(df["date"])

    load_weather_data(df)


@task
def validate_task():
    count = get_record_count("TT_DATABASE.RAW.WEATHER_DATA")

    print(f"Number of records: {count}")


with DAG(
    dag_id="TokyoWeather",
    start_date=datetime(
        2026,
        9,
        1,
        tzinfo=ZoneInfo("Asia/Tokyo"),
    ),
    catchup=False,
    schedule=None,
    tags=["ETL"],
) as dag:
    latitude = Variable.get("LATITUDE")
    longitude = Variable.get("LONGITUDE")

    raw_data = extract_task(
        latitude,
        longitude,
    )

    transformed_data = transform_task(
        raw_data,
        latitude,
        longitude,
    )

    loaded = load_task(transformed_data)

    validation = validate_task()

    loaded >> validation
