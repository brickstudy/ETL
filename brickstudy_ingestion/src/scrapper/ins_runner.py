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

twitter_keyword = [
    "닥터지", "아이소이", "에뛰드", "에스트라", "유세린", "토리든"
]


def get_brand_lst_wo_ingested_list():
    brand_lst = get_brand_list_fr_s3()
    with open(f"{base_path}/results/finished_brand.txt", "r") as f:
        skip = f.read()
    return list(set(brand_lst) - set(skip[:-1].split('\n')))


def crawl_data(brand_lst: list, err: int):
    """
    brand_lst 에 속한 brand이 언급된 데이터를 인스타그램으로부터 수집하여
    ./results/data, ./results/images에 저장하는 함수
    :brand_lst: 크롤링할 서치 키워드가 담긴 리스트
    :err: 크롤링 진행 과정에서 발생한 오류 횟수
    """
    for brand in brand_lst:
        if err > 10:
            break

        crawler = InsURLCrawler(dev=True)
        crawler.get_urls(keyword=brand)
        crawler.materialize()
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
            with open(f"{post_crawler.base_path}/results/finished_brand.txt", "a") as f:
                f.write(f"{brand}\n")
        except Exception as e:
            logging.error(
                "{} data write 과정에서 오류 발생. \nerror message: {}".format(brand, e)
            )

    return err


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
    base_path = "/Users/seoyeongkim/Documents/ETL/brickstudy_ingestion/src/scrapper/"
    # shutil.rmtree(base_path + "results/data")
    # shutil.rmtree(base_path + "results/images")
    # os.mkdir(base_path + "results/data")
    # os.mkdir(base_path + "results/images")

    err = 0
    # brand_lst = get_brand_lst_wo_ingested_list()

    brand_lst = twitter_keyword
    for block_s in range(0, len(brand_lst), 10):
        partitioned = brand_lst[block_s:block_s + 10]
        print(f"**** start crawling {partitioned} ****")
        err += crawl_data(brand_lst[block_s:block_s + 10], err)

    # s3_upload(base_path + "results", 'data')
    # s3_upload(base_path + "results", 'images')


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