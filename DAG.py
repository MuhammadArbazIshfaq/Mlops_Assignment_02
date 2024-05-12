from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 5, 12),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG object
dag = DAG(
    'hello_airflow',
    default_args=default_args,
    description='A simple Airflow DAG to print "Hello, Airflow!"',
    schedule_interval=timedelta(days=1),  # Run the DAG daily
)

# Define the task
print_hello_task = BashOperator(
    task_id='print_hello',
    bash_command='echo "Hello, Airflow!"',
    dag=dag,
)

# Set task dependencies
print_hello_task
