from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime, timedelta
import pendulum

default_args = {
    'owner':'BreadFeet',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

def greet(ti):   # ti: task instance, reserved name
    first_name = ti.xcom_pull(task_ids='get_name', key='first_name')
    last_name = ti.xcom_pull(task_ids='get_name', key='last_name')
    age = ti.xcom_pull(task_ids='get_age', key='age')
    print(f'hello world! My name is {first_name} {last_name}, and I am {age} years old.')

# Return values or pushed values saved in XCom
def get_name(ti):
    ti.xcom_push(key='first_name', value='Jerry')
    ti.xcom_push(key='last_name', value='Fridman')

def get_age(ti):
    ti.xcom_push(key='age', value=19)

with DAG(
    default_args=default_args,    # Applied to all tasks in the DAG
    dag_id='example_python_operator',
    description='DAG using python operator',
    start_date=pendulum.datetime(2025, 10, 16, tz='Asia/Seoul'),
    schedule='@daily'
) as dag:

    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet,
        # op_kwargs={'age':20}   # Parameters for the function
    )

    task2= PythonOperator(
        task_id='get_name',
        python_callable=get_name,
    )

    task3 = PythonOperator(
        task_id='get_age',
        python_callable=get_age
    )

    # Task dependencies
    [task2, task3] >> task1