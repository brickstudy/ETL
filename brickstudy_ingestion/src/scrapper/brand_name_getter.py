import json

from src.common.aws.s3_uploader import S3Uploader
from src.scrapper.models import OliveyoungBrand


def get_latest_dt():
    return '2024-08-20'


def category_checker(category: list) -> bool:
    """
    standard 기준 카테고리에 하나라도 속해있으면 True 반환, 아니라면 False 반환
    """
    compare = set([c.split('_')[0] for c in category])
    standard = {'메이크업', '스킨케어', '향수', '헤어케어', '바디케어', '마스크팩', 
                '클렌징', '선케어', '더모코스메틱', '맨즈케어'}
    if len(compare & standard) > 0:
        return True
    return False


def filter_brand(file_content: str) -> list:
    filtered = []
    for line in file_content.split('\n'):
        if line == '':
            break
        for brandname, brandinfo in json.loads(line).items():
            brandinfo_dic = OliveyoungBrand(**brandinfo)
            if category_checker(brandinfo_dic.category):
                filtered.append(brandname)
    return filtered


def get_brand_list_fr_s3():
    s3_client = S3Uploader().s3_client
    bucket = 'brickstudy'

    def file_keys_getter():
        paginator = s3_client.get_paginator('list_objects_v2')
        prefix = f"bronze/viral/oliveyoung/{get_latest_dt()}"
        file_key_lst = []
        for page in paginator.paginate(
            Bucket=bucket,
            Prefix=prefix
        ):
            if 'Contents' in page:
                for obj in page['Contents']:
                    file_key_lst.append(obj['Key'])
        return file_key_lst

    file_key_lst = file_keys_getter()
    filtered_brand_lst = []
    for filekey in file_key_lst:
        response = s3_client.get_object(
            Bucket=bucket,
            Key=filekey
        )
        file_content = response['Body'].read().decode('utf-8')
        filtered_brand_lst += filter_brand(file_content)
    return filtered_brand_lst