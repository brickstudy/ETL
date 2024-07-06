from datetime import timedelta
from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator

from src.naver.naver_search import NaverSearch

# aiflow setting
default_args = {
    'owner': 'brickstudy',
    'start_date': days_ago(0),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}


# task setting
def request_naver_api():
    target_platform = "news"
    query = "여행"
    client = NaverSearch(target_platform)
    result = client.request_with_keword(query)
    print(result)


with DAG(
    dag_id='naver_search_api_news',
    default_args=default_args,
    description='sample dag for fetching data from naver news via NaverAPI',
    schedule_interval='@daily',
):
    extract_task = PythonOperator(
        task_id="request_naver_api",
        python_callable=request_naver_api
    )

    extract_task
