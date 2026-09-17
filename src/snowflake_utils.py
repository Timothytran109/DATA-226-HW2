from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook


def get_snowflake_connection():
    hook = SnowflakeHook(snowflake_conn_id="snowflake_conn")

    return hook.get_conn()
