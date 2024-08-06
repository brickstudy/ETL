from datetime import datetime
import multiprocessing
import uuid

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.scrapper.oliveyoung import Brand
from src.scrapper.utils import (
    dict_partitioner,
    write_local_as_json,
)


DAG_ID = "bronze_viral_oliveyoung"
CONCURRENCY_LEVEL = multiprocessing.cpu_count()

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1)
}


def entrypoint():
    brand = Brand()
    brand.crawl_brand_metadata()
    for partitioned_data in dict_partitioner(
        data=brand.brand_metadata,
        level=CONCURRENCY_LEVEL
    ):
        with multiprocessing.Pool(CONCURRENCY_LEVEL) as p:
            p.map(get_item, partitioned_data)


def get_item(data: dict):
    brand = Brand(data)
    brand.crawl_items()
    file_name = 'brand_item_data_' + uuid.uuid4()
    write_local_as_json(data=brand.brand_metadata, file_name=file_name)


with DAG(
    dag_id=DAG_ID,
    default_args=default_args,
    schedule_interval='@daily'
):

    task1 = PythonOperator(
        task_id='get_brand_metadata',
        python_callable=entrypoint
    )

    task1
