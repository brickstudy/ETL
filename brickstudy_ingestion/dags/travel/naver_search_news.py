from datetime import timedelta
import boto3

from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator

from src.naver.naver_search import NaverSearch
from src.common.aws.s3_uploader import S3Uploader
from dags.config import (
    NAVER_API_CLIENT_ID,
    NAVER_API_CLIENT_SECERT,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    S3_BUCKET_NAME
)

DAG_ID = 'bronze_travel_naverapi'
TARGET_PLATFORM = "news"
QUERY = "여행"


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
    client = NaverSearch(
        client_id=NAVER_API_CLIENT_ID,
        client_secret=NAVER_API_CLIENT_SECERT,
        target_platform=TARGET_PLATFORM
    )
    return client.request_with_keyword(
        query=QUERY,
        display=100
    )


def upload_to_s3(data):
    timestamp = data["lastBuildDate"]
    s3_client = boto3.client(
        "s3", 
        aws_access_key_id=AWS_ACCESS_KEY_ID, 
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    s3_uploader = S3Uploader(s3_client)
    s3_uploader.write_s3(
        bucket_name=S3_BUCKET_NAME,
        file_key=f"{DAG_ID.replace('_', '/')}/{TARGET_PLATFORM}_{timestamp}",
        data_type='json',
        data=data["items"][0]
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
