from datetime import timedelta

from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator

from dags.utils.utils import request_naver_api, upload_to_s3

DAG_ID = "bronze_travel_naverapi"
TARGET_PLATFORM = 'news'
QUERY = '여행'


# aiflow setting
default_args = {
    'owner': 'brickstudy',
    'start_date': days_ago(0),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}


# task setting
def fetch_and_store():
    data = request_naver_api()
    file_s3_path = f"{DAG_ID.replace('_', '/')}/{TARGET_PLATFORM}_{data['lastBuildDate']}"
    upload_to_s3(file_key=file_s3_path, data=data["items"][0])


with DAG(
    dag_id=DAG_ID,
    default_args=default_args,
    description='sample dag for fetching data from naver news via NaverAPI',
    schedule_interval='@daily',
):
    extract_task = PythonOperator(
        task_id="request_naver_api",
        python_callable=fetch_and_store
    )

    extract_task
