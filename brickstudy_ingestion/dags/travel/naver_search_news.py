from datetime import timedelta, datetime

from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator

from src.naver.naver_search import NaverSearch
from src.common.aws.s3_uploader import S3Uploader

TARGET_PLATFORM = "news"
QUERY = "여행"
BASE_PATH = "travel/bronze/naverAPI/news"
BUCKET_NAME = "brickstudy"


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
    upload_to_s3(data)


def request_naver_api():
    client = NaverSearch(TARGET_PLATFORM)
    return client.request_with_keyword(
            query=QUERY,
            display=100
        )


def upload_to_s3(data):
    timestamp = datetime.strftime(data["lastBuildDate"], "%a, %d %b %Y %H:%M:%S %z").timestamp()
    s3_uploader = S3Uploader()
    s3_uploader.write_s3(
        bucket_name=BUCKET_NAME,
        file_key=f"{BASE_PATH}/{timestamp}",
        data_type='json',
        data=data["items"][0]
    )


with DAG(
    dag_id='naver_search_api_news',
    default_args=default_args,
    description='sample dag for fetching data from naver news via NaverAPI',
    schedule_interval='@daily',
):
    extract_task = PythonOperator(
        task_id="request_naver_api",
        python_callable=fetch_and_store
    )

    extract_task
