from datetime import timedelta

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.decorators import task
from airflow.operators.python import PythonVirtualenvOperator

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


def entrypoint():
    import logging
    import multiprocess
    from src.common.kafka.utils import Kafka
    from src.scrapper.inscrawler import InsCrawler
    from src.scrapper.ins_url import InsURLCrawler
    from src.scrapper.ins_data import InsDataCrawler

    brand_lst = get_brand_list_fr_s3
    CONCURRENCY_LEVEL = multiprocess.cpu_count()

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
        with multiprocess.Pool(CONCURRENCY_LEVEL) as p:
            p.map(crawl_instagram, brand_lst)
    except Exception as e:
        logging.error("***entrypoint error***", e)
        raise

with DAG(
    dag_id=DAG_ID,
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
):
    t_crawl_ins = PythonVirtualenvOperator(
        task_id='crawl_instagram_based_on_keyword',
        python_version='3.10',
        system_site_packages=False,
        requirements=['selenium==4.24.0', 'webdriver-manager==4.0.2',
                      'bs4==0.0.2', 'beautifulsoup4==4.12.3',
                      'lxml==5.3.0', 'pytz==2024.1',
                      "python-dotenv==0.19.0", "multiprocess", "kafka-python"],
        python_callable=entrypoint
    )