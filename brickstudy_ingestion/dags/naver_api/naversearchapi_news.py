# from datetime import timedelta
# from airflow.models import DAG
# from airflow.utils.dates import days_ago
# from airflow.operators.python import PythonOperator

# from brickstudy_ingestion.src.naver_api import NaverSearchAPI
# from brickstudy_ingestion.utils.airflow_utils import *

# def naver_api_call():
#     current_cnt = check_quota()
#     if current_cnt <= 25000:
#         NewsAPI = NaverSearchAPI()
#         NewsAPI.request_with_keyword('여행') #TODO argument로 키워드 주입할 수 있도록 refactor
#         update_quota(current_cnt)

# default_args = {
#     'owner': 'brickstudy',
#     'start_date': days_ago(0),           #When this DAG should run from(days_ago(0) means today)
#     'retries': 1,                        #The number of retries in case of failure
#     'retry_delay': timedelta(minutes=5), #The time delay between retries
# }

# dag = DAG(
#     dag_id='naver_search_api_news',
#     default_args=default_args,            # the default arguments to apply to your DAG
#     description='sample dag for fetching data from naver news via NaverAPI',
#     schedule_interval='@daily',           # how frequently this DAG runs(everyday)
# )

# t1 = PythonOperator(
#     task_id='query_naver_api',
#     python_callable=naver_api_call,
#     dag=dag,
# )

# t1
