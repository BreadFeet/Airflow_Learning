from datetime import datetime, timedelta
import pendulum

from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

default_args = {
    'owner':'BreadFeet',
    'retries':5,
    'retry_delay':timedelta(minutes=5)
}

with DAG(
    default_args=default_args,
    dag_id='dag_with_minio_s3_v04',
    start_date=pendulum.datetime(2025, 11, 15, tz="Asia/Seoul"),
    schedule='@daily'
) as dag:

    # Sensor to check for the presence of a file (key) in MinIO S3
    task1 = S3KeySensor(
        task_id='minio_sensor_s3',
        bucket_name='airflow',
        bucket_key='data.csv',   # Key: file-like instance on S3
        aws_conn_id='minio_conn',
        mode='poke',
        poke_interval=5,
        timeout=30 
    )