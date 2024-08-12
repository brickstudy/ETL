from datetime import timedelta, datetime

from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator

from src.naver.naver_search import NaverSearch
from src.common.aws.s3_uploader import S3Uploader
from dags.utils.config import set_env_variables
from dags.utils.discord_message import on_failure_callback

# =========================================
# Set env variables
set_env_variables()

# Change parameter
DAG_ID = "bronze_travel_naversearch"
TARGET_PLATFORM = 'news'
QUERY = '여행'

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
def fetch_and_store():
    data = request_naver_api()
    upload_to_s3(data)


def request_naver_api():
    client = NaverSearch(
        target_platform=TARGET_PLATFORM
    )
    return client.request_with_keyword(
        query=QUERY,
        display=100
    )


def upload_to_s3(data):
    timestamp = datetime.now().strftime("%Y-%m-%d")
    s3_uploader = S3Uploader()
    s3_uploader.write_s3(
        file_key=f"{DAG_ID.replace('_', '/')}/{timestamp}/{TARGET_PLATFORM}.json",
        data_type='json',
        data=data
    )


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
