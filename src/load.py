from src.snowflake_utils import get_snowflake_connection


def load_weather_data(df):
    conn = get_snowflake_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS TT_DATABASE.RAW.weather_data (
                latitude FLOAT NOT NULL,
                longitude FLOAT NOT NULL,
                date DATE NOT NULL,
                temp_max FLOAT,
                temp_min FLOAT,
                precipitation FLOAT,
                weather_code INT,
                PRIMARY KEY (latitude, longitude, date)
            );
            """
        )

        cursor.execute("BEGIN;")

        cursor.execute(
            """
            DELETE FROM TT_DATABASE.RAW.weather_data;
            """
        )

        insert_query = """
            INSERT INTO TT_DATABASE.RAW.weather_data (
                latitude,
                longitude,
                date,
                temp_max,
                temp_min,
                precipitation,
                weather_code
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """

        for _, row in df.iterrows():
            cursor.execute(
                insert_query,
                (
                    row["latitude"],
                    row["longitude"],
                    row["date"].date(),
                    row["temp_max"],
                    row["temp_min"],
                    row["precipitation"],
                    row["weather_code"],
                ),
            )

        cursor.execute("COMMIT;")

    except Exception:
        cursor.execute("ROLLBACK;")
        raise

    finally:
        cursor.close()
        conn.close()
