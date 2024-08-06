from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonVirtualenvOperator

from src.scrapper.oliveyoung import Brand
from src.scrapper.utils import (
    # dict_partitioner,
    write_local_as_json,
)


DAG_ID = "bronze_viral_oliveyoung"

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1)
}


def entrypoint():
    import logging
    import multiprocessing
    import uuid
    from src.scrapper.oliveyoung import Brand
    from src.scrapper.utils import dict_partitioner

    CONCURRENCY_LEVEL = multiprocessing.cpu_count()

    def get_item(data: dict):
        brand = Brand(data)
        brand.crawl_items()
        file_name = 'brand_item_data_' + uuid.uuid4()
        write_local_as_json(data=brand.brand_metadata, file_name=file_name)

    try:
        brand = Brand()
        brand.crawl_brand_metadata()
        partitioned_data = dict_partitioner(
            data=brand.brand_metadata,
            level=CONCURRENCY_LEVEL
        )
        with multiprocessing.Pool(CONCURRENCY_LEVEL) as p:
            p.map(get_item, partitioned_data)
        # get_item(partitioned_data)
    except Exception as e:
        logging.error("***entrypoint error***", e)
        raise


with DAG(
    dag_id=DAG_ID,
    default_args=default_args,
    schedule_interval='@daily'
):

    task1 = PythonVirtualenvOperator(
        task_id='get_brand_metadata',
        python_version='3.7',
        system_site_packages=False,
        requirements=["beautifulsoup4==4.9.3", "python-dotenv==0.19.0"],
        python_callable=entrypoint
    )

    task1
