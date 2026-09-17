from src.snowflake_utils import get_snowflake_connection


def get_record_count(table):
    conn = get_snowflake_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        result = cursor.fetchone()

        return result[0]

    finally:
        cursor.close()
        conn.close()
