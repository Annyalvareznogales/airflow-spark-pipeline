from airflow.providers.postgres.hooks.postgres import PostgresHook


def create_processed_tables():
    hook = PostgresHook(postgres_conn_id="postgres_conn")

    conn = hook.get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE SCHEMA IF NOT EXISTS processed;
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS processed.example (
            fiscal_year int,
            title_description varchar(200),
            regular_hours float,
            regular_gross_paid float
        );
    """)

    conn.commit()
    cur.close()
