#Taskflow API simplifies the code by removing the need for XComs and making dependencies clearer.
from airflow.decorators import dag, task   # Decorators of Taskflow API
from datetime import datetime, timedelta
import pendulum

default_args = {
    'owner':'BreadFeet',
    'retries': 5,
    'retry_delay':timedelta(minutes=5)
}

@dag(dag_id='dags_with_taskflow_api_v02',
     default_args=default_args,
     start_date=pendulum.datetime(2025, 10, 17, tz='Asia/Seoul'),
     schedule='@daily')

def hello_world_etl():
    
    @task(multiple_outputs=True)
    def get_name():
        return {
            'first_name': 'Jerry',
            'last_name': 'Fridman'
        }

    @task
    def get_age():
        return 19

    @task
    def greet(first_name, last_name, age):
        print(f'Hello world! My name is {first_name} {last_name}, and I am {age} years old!')

    name_dict = get_name()
    age = get_age()
    greet(first_name=name_dict['first_name'], 
          last_name=name_dict['last_name'], 
          age=age)

# Run the tasks
dag_greet = hello_world_etl()