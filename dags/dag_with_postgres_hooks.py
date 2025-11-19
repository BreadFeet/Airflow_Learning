import csv
import logging

from datetime import datetime, timedelta
import pendulum
from tempfile import NamedTemporaryfile

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

default_args = {
    'owner':'BreadFeet',
    'retries':5,
    'retry_delay':timedelta(minutes=5)
}

def postgres_to_s3(ds, data_interval_end, ds_nodash):
    # step 1: query data from postgresql and save it as a text file
    hook = PostgresHook(postgres_conn_id='postgres_localhost')
    conn = hook.get_conn()
    cursor = conn.cursor()
    end = data_interval_end + timedelta(days=1)
    end = end.strftime('%Y%m%d')
    # Using ds (with dash) or ds_nodash yields the same result.
    cursor.execute(
        f"""
        SELECT * FROM orders WHERE date >= '{ds}' and date < '{end}'
        """
    )
    # The file path is Airflow container directory. Make sure the path exists.
    with NamedTemporaryfile(mode='w', suffix=f'{ds_nodash}') as f:
    # with open(f'dags/get_orders_{ds_nodash}.txt', 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([i.name for i in cursor.description])   # cursor.description: column names
        csv_writer.writerows(cursor)
        f.flush()    # Save data from buffer to the file while the file is still open.
    cursor.close()
    conn.close() 
    logging.info(f"Saved query results in get_orders_{ds_nodash}.txt")

    # step 2: upload the file to S3 bucket
    # For MinIO connection, docker network connection between Airflow and MinIO should be set.
    s3_hook = S3Hook(aws_conn_id='minio_conn')
    s3_hook.load_file(
        filename=f'dags/get_orders_{ds_nodash}.txt',
        bucket_name = 'airflow',
        key=f'orders/{ds_nodash}.txt',
        replace=True
    )
    
with DAG(
    default_args=default_args,
    dag_id='dag_with_postgres_hooks_v03',
    start_date=pendulum.datetime(2025, 11, 18, tz='Asia/Seoul'),
    schedule='@daily'
) as dag:

    task1 = PythonOperator(
        task_id='postgres_to_s3',
        python_callable=postgres_to_s3
    )