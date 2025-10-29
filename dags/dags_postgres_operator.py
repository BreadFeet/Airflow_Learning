from airflow import DAG
# PostgresOperator is deprecated, use SQLExecuteQueryOperator instead
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

from datetime import datetime, timedelta
import pendulum

default_args = {
    'owner':'BreadFeet',
    'retries':5,
    'retry_delay':timedelta(minutes=5)
}

with DAG(
    default_args=default_args,
    dag_id='example_postgres_operator_v11',
    start_date=pendulum.datetime(2025, 10, 24, tz='Asia/Seoul'),
    schedule='6 0 * * *'  
) as dag:

    task1 = SQLExecuteQueryOperator(
        task_id='create_postgres_table',
        conn_id='postgres_localhost',
        sql='''
            create table if not exists dag_runs(
                dt date,
                dag_id character varying,
                primary key (dt, dag_id)
            )    
        '''
    )

    # Delete before insert to avoid primary key conflict
    task2 = SQLExecuteQueryOperator(
        task_id='delete_from_table',
        conn_id='postgres_localhost',
        sql='''
             delete from dag_runs where dt = '{{ds}}'and dag_id = '{{dag.dag_id}}'  
        '''   # Template variables
    )

    task3 = SQLExecuteQueryOperator(
        task_id='insert_into_table',
        conn_id='postgres_localhost',
        sql='''
            insert into dag_runs (dt, dag_id) values ('{{ds}}', '{{dag.dag_id}}')  
        '''   # Template variables
    )

    task1 >> task2 >> task3