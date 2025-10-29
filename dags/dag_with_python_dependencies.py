from airflow.decorators import dag, task

from datetime import datetime, timedelta
import pendulum

default_args = {
    'owner':'BreadFeet',
    'retries':5,
    'retry_delay':timedelta(minutes=5)
}

@dag(
    default_args=default_args,
    dag_id='example_python_dependencies_v02',
    start_date=pendulum.datetime(2025, 10, 29, tz='Asia/Seoul'),
    schedule='@daily'
)

def python_dependencies_etl():

    @task
    def get_sklearn():
        import sklearn 
        print(f'scikit-learn version:{sklearn.__version__}')

    @task
    def get_matplotlib():
        import matplotlib
        print(f'matplotlib version:{matplotlib.__version__}')   

    get_sklearn()
    get_matplotlib()

python_dependencies_etl()    