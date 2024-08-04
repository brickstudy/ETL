import pytest
import boto3
import moto

from src.common.aws.s3_uploader import S3Uploader


PLATFROM = "news"
QUERY = "여행"


@pytest.fixture(scope='session')
def mock_session():
    with moto.mock_aws():
        session = boto3.Session(
            aws_access_key_id='fake_id',
            aws_secret_access_key='fake_secret',
            region_name='ap-northeast-2'
        )
        bucket_name = 'testBucket'
        config = {'LocationConstraint': 'ap-northeast-2'}
        s3 = session.client('s3')
        s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=config)
        yield s3


def test_naver_search_can_connect_to_aws(mock_session):
    import json
    from datetime import datetime

    # given : valid s3 client id, password
    # when : request that trying to connect aws
    # then : task success
    data = {'lastBuildDate': 'Sun, 21 Jul 2024 21:14:41 +0900',
            'total': 5414727,
            'start': 1,
            'display': 1,
            'items': [{'title': '[단독]한전, 건설지역서 10년간 선심성 식사·<b>여행</b> 등에 25억 이상 썼다',
                    'originallink': 'https://www.khan.co.kr/economy/economy-general/article/202407211426001',
                    'link': 'https://n.news.naver.com/mnews/article/032/0003309729?sid=101',
                    'description': '대부분 주민에게 식사와1 기념품, <b>여행</b>을 제공하는 데 사용됐다. 한 끼에 850만원이 넘는 금액이 결제되거나, ... ',
                    'pubDate': 'Sun, 21 Jul 2024 14:27:00 +0900'}]}
    json_data = json.dumps(data)

    s3uploader = S3Uploader(mock_session)

    id = datetime.today().strftime("%Y-%m-%d %H:%M:%S.%f")
    s3uploader.write_s3(
        bucket_name='testBucket',
        file_key=f'{PLATFROM}_{QUERY}_{id}',
        data_type='json',
        data=json_data
    )

    assert s3uploader.s3_client.head_object(
        Bucket='testBucket',
        Key=f'{PLATFROM}_{QUERY}_{id}'
    )


def test_s3_uploader_mime_get_right_content_type(mock_session):
    # given : 올바른 data type
    extension = "json"
    # when : put_object()의 ContentType 옵션에 들어갈 파일 타입 받아오기
    # then : 알맞게 매핑된 ContentType
    obj = S3Uploader(mock_session)
    assert obj.get_mime_type(extension) == 'application/json'


def test_s3_uploader_mime_get_incorrect_content_type(mock_session):
    # given : 올바르지 않은 data type
    extension = "wrong"
    # when : put_object()의 ContentType 옵션에 들어갈 파일 타입 받아오기
    # then : raise Value Error
    with pytest.raises(ValueError):
        obj = S3Uploader(mock_session)
        error = obj.get_mime_type(extension)
        assert error['message'] == "Unsupported file extension."
