from src.scrapper.brand_name_getter import get_brand_list_fr_s3
from src.scrapper.ins_url import InsURLCrawler
from src.scrapper.ins_data import InsDataCrawler
from src.common.aws.s3_uploader import S3Uploader
from src.scrapper.utils import write_local_as_json
from src.scrapper.utils import current_datetime_getter
import logging
import os

logger = logging.getLogger('insrunner')
logger.setLevel(logging.ERROR)


def crawl_data():
    brand_lst = get_brand_list_fr_s3()
    for brand in brand_lst:
        try:
            crawler = InsURLCrawler(dev=True)
            crawler.get_urls(keyword=brand)
            crawler.materialize()
        except Exception as e:
            logging.error(
                "{} url 수집 과정에서 오류 발생. \nerror message: {}".format(brand, e)
            )
        finally:
            pass

        try:
            post_crawler = InsDataCrawler(
                driver=crawler.driver,
                data=crawler.data,
                dev=True
            )
            post_crawler.get_post_data()
        except Exception as e:
            logging.error(
                "{} post data 수집 과정에서 오류 발생. \nerror message: {}".format(brand, e)
            )
        finally:
            pass

        try:
            write_local_as_json(
                data=post_crawler.data,
                file_path=f"{post_crawler.base_path}/results/data",
                file_name=f"instagram_{current_datetime_getter}"
            )
        except Exception as e:
            logging.error(
                "{} data write 과정에서 오류 발생. \nerror message: {}".format(brand, e)
            )
        finally:
            pass

    return f"{post_crawler.base_path}/results/data"


def s3_upload(local_path):
    s3 = S3Uploader().s3_client
    s3_path = "bronze/viral/instagram",
    bucket_name = "brickstudy"

    for root, _, files in os.walk(local_path):
        for file in files:
            local_file_path = os.path.join(root, file)
            # S3 파일 경로 설정
            s3_file_path = os.path.join(s3_path, os.path.relpath(local_file_path, local_path))

            try:
                s3.upload_file(local_file_path, bucket_name, s3_file_path)
                print(f"File {local_file_path} uploaded to {bucket_name}/{s3_file_path}")
            except FileNotFoundError:
                print(f"File not found: {local_file_path}")
            except Exception as e:
                print(f"Failed to upload {local_file_path}: {str(e)}")


if __name__ =='__main__':
    local_path = crawl_data()
    s3_upload(local_path)

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