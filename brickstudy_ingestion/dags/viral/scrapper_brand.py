from datetime import datetime
import os
import json
import requests
import logging

from airflow import DAG
from airflow.operators.python import PythonVirtualenvOperator, PythonOperator

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
def kafka_to_s3():
    KAFKA_CONNECT = "kafka-connect"
    url = f'http://{KAFKA_CONNECT}:8083/connectors/sink-s3-voluble/config'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    data = {
        "connector.class": "io.confluent.connect.s3.S3SinkConnector",
        "key.converter": "org.apache.kafka.connect.storage.StringConverter",
        "tasks.max": 1,
        "topics": "oliveyoung",
        "s3.region": "ap-northeast-1",
        "s3.bucket.name": "brickstudy",
        "s3.credentials.provider.class": "AwsAssumeRoleCredentialsProvider",
        "flush.size": 65536,
        "storage.class": "io.confluent.connect.s3.storage.S3Storage",
        "format.class": "io.confluent.connect.s3.format.avro.AvroFormat",          
        "topics.dir": f"{DAG_ID.replace('_', '/')}",
        "locale": "ko_KR",
        "timezone": "Asia/Seoul"
    }
        # 	"schema.generator.class": "io.confluent.connect.storage.hive.schema.DefaultSchemaGenerator",
        # 	"schema.compatibility": "NONE",
        #     "partitioner.class": "io.confluent.connect.storage.partitioner.DefaultPartitioner",
        #     "transforms": "AddMetadata",
        #     "transforms.AddMetadata.type": "org.apache.kafka.connect.transforms.InsertField$Value",
        #     "transforms.AddMetadata.offset.field": "_offset",
        #     "transforms.AddMetadata.partition.field": "_partition"
        # }

    response = requests.put(url, headers=headers, data=json.dumps(data))
    print(response)


with DAG(
    dag_id=DAG_ID,
    default_args=default_args,
    schedule_interval='@weekly'
):

    # task1 = PythonVirtualenvOperator(
    #     task_id='get_brand_metadata',
    #     python_version='3.7',
    #     system_site_packages=False,
    #     requirements=["beautifulsoup4==4.9.3", "python-dotenv==0.19.0", "multiprocess", "kafka-python"],
    #     python_callable=entrypoint
    # )

    task3 = PythonOperator(
        task_id="upload_brand_json_file_to_s3",
        python_callable=kafka_to_s3
    )

    task3


"""


curl -i -X PUT -H "Accept:application/json" \
    -H  "Content-Type:application/json" http://kafka-connect:8083/connectors/sink-s3-voluble/config \
    -d '
 {"connector.class": "io.confluent.connect.s3.S3SinkConnector",
    "key.converter": "org.apache.kafka.connect.storage.StringConverter",
    "tasks.max": 1,
    "topics": "oliveyoung",
    "s3.region": "ap-northeast-2",
    "s3.bucket.name": "brickstudy",
    "s3.credentials.provider.class": "AwsAssumeRoleCredentialsProvider",
    "topics.dir": "bronze/viral/oliveyoung",
    "flush.size": 65536,
    "storage.class": "io.confluent.connect.s3.storage.S3Storage",
    "format.class": "io.confluent.connect.s3.format.json.JsonFormat"
}'

"""