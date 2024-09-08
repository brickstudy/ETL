from src.scrapper.brand_name_getter import get_brand_list_fr_s3
from src.scrapper.ins_url import InsURLCrawler
from src.scrapper.ins_data import InsDataCrawler
from src.scrapper.utils import write_local_as_json
from src.scrapper.utils import current_datetime_getter
import os
import logging
import subprocess

logger = logging.getLogger('insrunner')
logger.setLevel(logging.ERROR)


def crawl_data():
    brand_lst = get_brand_list_fr_s3()
    err = 0
    for brand in brand_lst[13:]:
        if err > 10: 
            break

        crawler = InsURLCrawler(dev=True)
        crawler.get_urls(keyword=brand)
        err += crawler.numof_error

        post_crawler = InsDataCrawler(
            driver=crawler.driver,
            data=crawler.data,
            dev=True
        )
        post_crawler.get_post_data()
        err += post_crawler.numof_error

        try:
            cur_date = current_datetime_getter()
            write_local_as_json(
                data=post_crawler.data,
                file_path=f"{post_crawler.base_path}/results/data",
                file_name=f"instagram_{cur_date}"
            )
        except Exception as e:
            logging.error(
                "{} data write 과정에서 오류 발생. \nerror message: {}".format(brand, e)
            )

    return f"{post_crawler.base_path}/results"


def s3_upload(local_path: str, target: str = 'data'):
    local_folder = os.path.join(local_path, target)
    dt = current_datetime_getter()
    dt = dt.split('_')[0]
    s3_folder = f"bronze/viral/instagram/{dt[:4]}-{dt[4:6]}-{dt[6:]}/{target}"
    bucket_name = "brickstudy"
    try:
        subprocess.run(
            ['aws', 's3', 'cp', local_folder, f's3://{bucket_name}/{s3_folder}/', '--recursive'],
            check=True
        )
        print(f"Folder {local_folder} uploaded to s3://{bucket_name}/{s3_folder}/")
    except subprocess.CalledProcessError as e:
        print(f"Failed to upload folder: {str(e)}")


if __name__ == '__main__':
    local_path = crawl_data()
    s3_upload(local_path, 'data')
    s3_upload(local_path, 'images')

"""
curl -i -X PUT -H "Accept:application/json" -H  "Content-Type:application/json" http://kafka-connect:8083/connectors/sink-s3-voluble/config -d '{
    "connector.class": "io.confluent.connect.s3.S3SinkConnector",
    "key.converter": "org.apache.kafka.connect.storage.StringConverter",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "false",
    "tasks.max": 1,
    "topics": "instagram",
    "aws.signing_region": "ap-northeast-2", 
    "s3.part.size": 5242880,
    "s3.region": "ap-northeast-2",
    "s3.bucket.name": "brickstudy",
    "s3.credentials.provider.class": "com.amazonaws.auth.DefaultAWSCredentialsProviderChain",
    "topics.dir": "bronze/viral",
    "partitioner.class": "io.confluent.connect.storage.partitioner.TimeBasedPartitioner",
    "partition.duration.ms": "86400000",
    "timestamp.extractor": "Record",
    "path.format": "yyyy-MM-dd",
    "flush.size": 100,
    "rotate.interval.ms": 60000,
    "storage.class": "io.confluent.connect.s3.storage.S3Storage",
    "format.class": "io.confluent.connect.s3.format.json.JsonFormat",
    "locale": "ko_KR",
    "timezone": "Asia/Seoul"
}'
"""