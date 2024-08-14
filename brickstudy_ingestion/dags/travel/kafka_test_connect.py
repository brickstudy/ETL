from datetime import timedelta

from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonVirtualenvOperator

from dags.utils.discord_message import on_failure_callback

# =========================================
# Change parameter
DAG_ID = "bronze_travel_mock_randomuser"


# Set aiflow setting
default_args = {
    'owner': 'brickstudy',
    'start_date': days_ago(0),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'on_failure_callback': on_failure_callback,
}
# =========================================


# task setting
def fetch_and_send():
    # GET data
    def fetch_data_from_api(content):
        return {"test": content}

    data = fetch_data_from_api("test content 입니다.")

    # Send kafka cluster
    from src.common.kafka.utils import Kafka

    KAFKA_TOPIC = "mock-randomuser"

    producer = Kafka()
    producer.send_data_to_kafka(KAFKA_TOPIC, data)


with DAG(
    dag_id=DAG_ID,
    default_args=default_args,
    description='test dag to send kafka cluster',
    schedule_interval='@daily',
):
    extract_task = PythonVirtualenvOperator(
        task_id="request_mock_randomuser",
        python_version='3.7',
        system_site_packages=False,
        requirements=["python-dotenv==0.19.0", "kafka-python", "requests"],
        python_callable=fetch_and_send
    )

    extract_task
