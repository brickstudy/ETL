from datetime import timedelta

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonVirtualenvOperator, PythonOperator
from airflow.models import Variable

from src.scrapper.brand_name_getter import get_brand_list_fr_s3

# =========================================
# Change parameter
DAG_ID = "bronze_viral_instagram"
TARGET_PLATFORM = 'instagram'

# Set aiflow setting
default_args = {
    'owner': 'brickstudy',
    'start_date': days_ago(0),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    # 'on_failure_callback': on_failure_callback,
}
# =========================================


def get_brand_list():
    import os
    for ENV_VARIABLE in ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY']:
        os.environ[ENV_VARIABLE] = Variable.get(ENV_VARIABLE, "")
    return get_brand_list_fr_s3()


def instagram_crawling(brand_lst, id, pwd):
    import os
    import logging
    from src.common.kafka.utils import Kafka
    from src.scrapper.inscrawler import InsCrawler
    from src.scrapper.ins_url import InsURLCrawler
    from src.scrapper.ins_data import InsDataCrawler

    os.environ['INSTAGRAM_CLIENT_ID'] = id
    os.environ['INSTAGRAM_CLIENT_PASSWORD'] = pwd

    def crawl_instagram(keywords: tuple):
        crawler = InsURLCrawler(InsCrawler(keywords=keywords)).get_urls()
        post_crawler = InsDataCrawler(crawler.data)
        post_crawler.get_post_data()
        producer.send_data_to_kafka(
            kafka_topic='instagram',
            data=post_crawler.data
        )

    try:
        producer = Kafka()
        crawl_instagram(brand_lst)
    except Exception as e:
        logging.error("***entrypoint error***", e)
        raise


with DAG(
    dag_id=DAG_ID,
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
):
    t1 = PythonOperator(
        task_id='get_brand_list_from_s3',
        python_callable=get_brand_list
    )

    t2 = PythonVirtualenvOperator(
        task_id='crawl_instagram_based_on_keyword',
        system_site_packages=False,
        op_kwargs={
            'brand_lst': "{{ ti.xcom_pull(task_ids='get_brand_list_from_s3') }}",
            'id': Variable.get('INSTAGRAM_CLIENT_ID'),
            'pwd': Variable.get('INSTAGRAM_CLIENT_PASSWORD')
        },
        python_version='3.10',
        system_site_packages=False,
        requirements=['selenium==4.24.0', 'webdriver-manager==4.0.2',
                      'bs4==0.0.2', 'beautifulsoup4==4.12.3',
                      'lxml==5.3.0', 'pytz==2024.1',
                      "python-dotenv==0.19.0", "multiprocess", "kafka-python"],
        python_callable=instagram_crawling
    )

    t1 >> t2