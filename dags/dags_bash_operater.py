from airflow import DAG
from airflow.operators.bash import BashOperator
import datetime
import pendulum

with DAG(
    dag_id='example_bash_operator',
    schedule='30 12 * * *',
    start_date=pendulum.datetime(2025, 10, 9, tz='Asia/Seoul'),
    catchup=False,   # the time period between current and the start_date will not be run
    # dagrun_timeout=datetime.timedelta(minutes=60),
    tags=['example', 'example2'],
    # params={'example_key':'example_value'}   # Parameters for tasks under this DAG
) as dag:

    # Task is defined by Operators
    bash_t1 = BashOperator(
        task_id='bash_t1',
        bash_command='echo who am I?'
    )

    bash_t2 = BashOperator(
        task_id='bash_t2',
        bash_command='echo $HOSTNAME'
    )

    # Task ordering
    bash_t1 >> bash_t2  