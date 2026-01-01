from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow import DAG
import pandas as pd
from airflow.models import Variable
import os
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from plugins.python_scripts.ingestion import main
from plugins.python_scripts.data_processing import connection, process_data
from plugins.python_scripts.processed_setup import create_processed_tables

def APIToDB():

    dest_hook = PostgresHook(postgres_conn_id="postgres_conn") 

    df , create_sql_script = main()

    conn = dest_hook.get_conn()
    cur = conn.cursor()

    cur.execute("CREATE SCHEMA IF NOT EXISTS staging;")
    conn.commit()

    cur.execute(create_sql_script)
    conn.commit()
    cur.close()

    rows = list(df.itertuples(index=False , name=None))
    dest_hook.insert_rows(table = "staging.example", rows = rows)



def DBToDB():
    dest_hook = PostgresHook(postgres_conn_id="postgres_conn") 

    df = dest_hook.get_pandas_df(sql=f"select * from staging.example")

    spark = connection()

    df = process_data(spark=spark, df=df)

    rows = list(df.itertuples(index=False , name=None))
    dest_hook.insert_rows(table = "processed.example", rows = rows)



with DAG(
    dag_id = "APIToDBDags",
    schedule="@daily",
    start_date = datetime.now() - timedelta(days=1),
    tags=['dags'],
) as dag:


    start = EmptyOperator(task_id='start')
    end = EmptyOperator(task_id='end')  
        
    APIToDB_task = PythonOperator(
        task_id=f"APIToDBTask",
        python_callable = APIToDB   
    )

    setup_processed = PythonOperator(
    task_id="setup_processed",
    python_callable=create_processed_tables
    )

    DBToDBTask = PythonOperator(
        task_id=f"DBToDBTask",
        python_callable = DBToDB        
    )

    start >> APIToDB_task >> setup_processed >> DBToDBTask >> end