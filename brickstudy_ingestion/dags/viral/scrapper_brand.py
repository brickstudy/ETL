from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonVirtualenvOperator, PythonOperator

# from dags.utils.discord_message import on_failure_callback

# =========================================
# Change parameter
DAG_ID = "bronze_viral_oliveyoung"
TARGET_PLATFORM = "brand"

# Set aiflow setting
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    # 'on_failure_callback': on_failure_callback,
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


with DAG(
    dag_id=DAG_ID,
    default_args=default_args,
    schedule_interval='@weekly'
):

    task = PythonVirtualenvOperator(
        task_id='get_brand_metadata',
        python_version='3.7',
        system_site_packages=False,
        requirements=["beautifulsoup4==4.9.3", "python-dotenv==0.19.0", "multiprocess", "kafka-python"],
        python_callable=entrypoint
    )

    task


"""
curl -i -X PUT -H "Accept:application/json" \
    -H  "Content-Type:application/json" \
    http://kafka-connect:8083/connectors/sink-s3-voluble/config \
    -d '
 {
    "connector.class": "io.confluent.connect.s3.S3SinkConnector",
    "key.converter": "org.apache.kafka.connect.storage.StringConverter",
    "tasks.max": 1,
    "topics": "oliveyoung",
    "aws.signing_region": "ap-northeast-2",
    "s3.part.size": 5242880,
    "s3.region": "ap-northeast-2",
    "s3.bucket.name": "brickstudy",
    "s3.credentials.provider.class": "com.amazonaws.auth.DefaultAWSCredentialsProviderChain",
    "topics.dir": "bronze/viral",
    "partitioner.class": "io.confluent.connect.storage.partitioner.TimeBasedPartitioner",
    "path.format": "${topic}/${partitioned_date}",
    "partition.duration.ms": "86400000",
    "timestamp.extractor": "RecordField",
    "timestamp.field": "released_date"
    "flush.size": 100,
    "rotate.interval.ms": 60000,
    "storage.class": "io.confluent.connect.s3.storage.S3Storage",
    "format.class": "io.confluent.connect.s3.format.json.JsonFormat",
    "locale": "ko_KR",
    "timezone": "Asia/Seoul"
}'

curl -s http://kafka-connect:8083/connectors/sink-s3-voluble/status

"""