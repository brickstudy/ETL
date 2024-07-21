import pytest
from src.common.errorcode import Naver
from src.common.exception import ExtractError
from src.naver.naver_search import NaverSearch


# Mock
PLATFROM = "news"
RESPONSE_FORMAT = "json"
QUERY = "여행"  # 검색어. UTF-8로 인코딩되어야 합니다.
DISPLAY = 10    # 한 번에 표시할 검색 결과 개수(기본값: 10, 최댓값: 100)
START = 1   # 검색 시작 위치(기본값: 1, 최댓값: 1000)
SORT = "sim"    # 검색 결과 정렬 방법 - sim: 정확도순으로 내림차순 정렬(기본값) - date: 날짜순으로 내림차순 정렬


def test_nave_search_can_connect_client_with_valid():
    # given : 유효한 네이버 ID, SECRET KEY

    # when : Naver news api 요청
    client = NaverSearch(PLATFROM, RESPONSE_FORMAT)
    result = client.request_with_keword(QUERY, DISPLAY, START, SORT)

    # then : json 데이터 확인
    assert result["start"] == 1
    assert result["display"] == 10
    assert result["items"]
    assert result["items"][0]["title"]
    assert result["items"][0]["originallink"]
    assert result["items"][0]["link"]
    assert result["items"][0]["description"]
    assert result["items"][0]["pubDate"]


def test_naver_search_cannot_connect_client_with_invalid_id():
    # given : 잘못된 네이버 ID
    wrong_id = "wrong_id"

    # when : Naver news api 요청
    # then : errorcode
    with pytest.raises(ExtractError):
        client = NaverSearch(PLATFROM, RESPONSE_FORMAT)
        client.headers["X-Naver-Client-Id"] = wrong_id
        result = client.request_with_keword(QUERY, DISPLAY, START, SORT)

        assert result["message"] == Naver.AuthError.value["message"]
        # assert result["log"]["errorMessage"] == 'NID AUTH Result Invalid (1000) : Authentication failed. (인증에 실패했습니다.)'
        # assert result["log"]["errorCode"] == '024'


def test_naver_search_cannot_connect_client_with_invalid_secret_key():
    # given : 잘못된 네이버 ID
    wrong_secret = "wrong_secret"

    # when : Naver news api 요청
    # then : errorcode
    with pytest.raises(ExtractError):
        client = NaverSearch(PLATFROM, RESPONSE_FORMAT)
        client.headers["X-Naver-Client-Secret"] = wrong_secret
        result = client.request_with_keword(QUERY, DISPLAY, START, SORT)

        assert result["message"] == Naver.AuthError.value["message"]
        # assert result["log"]["errorMessage"] == 'NID AUTH Result Invalid (28) : Authentication failed. (인증에 실패했습니다.)'
        # assert result["log"]["errorCode"] == '024'


def test_naver_search_can_connect_to_aws():
    import os, json
    from datetime import datetime
    import boto3

    # given : valid s3 client id, password
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

    # when : request that trying to connect aws
    # then : task success
    client = NaverSearch(PLATFROM, RESPONSE_FORMAT)
    result = client.request_with_keword(QUERY, DISPLAY, START, SORT)

    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id, 
        aws_secret_access_key=aws_secret_access_key
    )
    bucket_name = 'brickstudy'
    id = datetime.today().strftime("%Y-%m-%d %H:%M:%S.%f")
    file_destination=f'travel/bronze/naverAPI/{PLATFROM}/'
    file_name=f'{PLATFROM}_{QUERY}_{id}'
    file_key=file_destination+file_name
 
    s3.put_object(
        Bucket=bucket_name, 
        Key=file_key, 
        Body=json.dumps(result),
        ContentType='application/json'
    )


