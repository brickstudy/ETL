from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonVirtualenvOperator, PythonOperator
from airflow.operators.bash_operator import BashOperator

from src.common.aws.s3_uploader import S3Uploader
from dags.utils.discord_message import on_failure_callback

# =========================================
# Change parameter
DAG_ID = "bronze_viral_oliveyoung"
TARGET_PLATFORM = "brand"

# Dag specific variables
BRAND_JSON_FILE_PATH = "/opt/airflow/logs/viral"
TIMESTAMP = datetime.now().strftime("%Y-%m-%d")
MERGED_JSON_FILE = f"brand_{TIMESTAMP}.json"

# Set aiflow setting
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'on_failure_callback': on_failure_callback,
}
# =========================================


# task1
def entrypoint():
    import logging
    import multiprocess
    from dataclasses import asdict
    from src.scrapper.oliveyoung import Brand
    from src.common.kafka.utils import Kafka

    CONCURRENCY_LEVEL = multiprocess.cpu_count()

    def get_item(data: tuple):
        brand = Brand({data[0]: data[1]})
        brand.crawl_items()
        json_data = {b_name: asdict(details) for b_name, details in brand.brand_metadata.items()}
        producer.send_data_to_kafka(
            kafka_topic='oliveyoung',
            data=json_data
        )

    try:
        brand = Brand()
        brand.crawl_brand_metadata()
        producer = Kafka()
        with multiprocess.Pool(CONCURRENCY_LEVEL) as p:
            p.map(get_item, list(brand.brand_metadata.items()))
    except Exception as e:
        logging.error("***entrypoint error***", e)
        raise


# task3
def upload_to_s3():
    s3 = S3Uploader()
    s3.s3_client.upload_file(
        Filename=f"{BRAND_JSON_FILE_PATH}/{MERGED_JSON_FILE}",
        Bucket="brickstudy",
        Key=f"{DAG_ID.replace('_', '/')}/{TIMESTAMP}/{TARGET_PLATFORM}.json",
    )


with DAG(
    dag_id=DAG_ID,
    default_args=default_args,
    schedule_interval='@weekly'
):

    task1 = PythonVirtualenvOperator(
        task_id='get_brand_metadata',
        python_version='3.7',
        system_site_packages=False,
        requirements=["beautifulsoup4==4.9.3", "python-dotenv==0.19.0", "multiprocess", "kafka-python"],
        python_callable=entrypoint
    )

    task2 = BashOperator(
        task_id='merge_json_files_into_single_json_file',
        bash_command="""
        jq -s 'flatten' {{ params.BRAND_JSON_FILE_PATH }}/*.json > {{ params.MERGED_JSON_FILE }}
        """,
        params={
            'BRAND_JSON_FILE_PATH': BRAND_JSON_FILE_PATH,
            'MERGED_JSON_FILE': MERGED_JSON_FILE
        }
    )

    task3 = PythonOperator(
        task_id="upload_brand_json_file_to_s3",
        python_callable=upload_to_s3
    )

    task4 = BashOperator(
        task_id="clear_local_path",
        bash_command="rm {{ params.BRAND_JSON_FILE_PATH }}/*",
        params={'BRAND_JSON_FILE_PATH': BRAND_JSON_FILE_PATH}
    )

    task1
