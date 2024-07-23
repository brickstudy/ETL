import pytest
from src.common.errorcode import Naver
from src.common.exception import ExtractError
from src.naver.naver_search import NaverSearch
from src.common.aws_s3_mime import EXTENSION_TO_MIME
from src.common.s3_uploader import S3Uploader

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
    import json
    from datetime import datetime

    # given : valid s3 client id, password
    # when : request that trying to connect aws
    # then : task success
    data = {'lastBuildDate': 'Sun, 21 Jul 2024 21:14:41 +0900', 'total': 5414727, 'start': 1, 'display': 1, 'items': [{'title': '[단독]한전, 건설지역서 10년간 선심성 식사·<b>여행</b> 등에 25억 이상 썼다', 'originallink': 'https://www.khan.co.kr/economy/economy-general/article/202407211426001', 'link': 'https://n.news.naver.com/mnews/article/032/0003309729?sid=101', 'description': '대부분 주민에게 식사와 기념품, <b>여행</b>을 제공하는 데 사용됐다. 한 끼에 850만원이 넘는 금액이 결제되거나, 하루 견학에 쓰인 버스 임차비로 1300만원이 지출된 사례도 있었다. 견학에 참여했던 한 주민은 “스무 명... ', 'pubDate': 'Sun, 21 Jul 2024 14:27:00 +0900'}]}
    json_data = json.dumps(data)

    s3uploader = S3Uploader()

    id = datetime.today().strftime("%Y-%m-%d %H:%M:%S.%f")
    s3uploader.write_s3(
        bucket_name='brickstudy',
        file_key=f'travel/bronze/naverAPI/{PLATFROM}/{PLATFROM}_{QUERY}_{id}',
        data_type='json',
        data=json_data
    )

    response = s3uploader.s3_client.get_object(
        Bucket='brickstudy',
        Key=f'travel/bronze/naverAPI/{PLATFROM}/{PLATFROM}_{QUERY}_{id}'
    )
    content = response['Body'].read().decode('utf-8')
    json_content = json.loads(content)

    assert json_content == data

#TODO s3_uploader, get_mimetype으로 대체
def test_s3_uploader_mime_get_right_content_type():
    # given : 올바른 data type
    extension = "json"
    # when : put_object()의 ContentType 옵션에 들어갈 파일 타입 받아오기
    # then : 알맞게 매핑된 ContentType
    obj = S3Uploader()
    assert obj.get_mime_type(extension) == 'application/json'


def test_s3_uploader_mime_get_incorrect_content_type():
    # given : 올바르지 않은 data type
    extension = "wrong"
    # when : put_object()의 ContentType 옵션에 들어갈 파일 타입 받아오기
    # then : raise Value Error
    with pytest.raises(ValueError):
        obj = S3Uploader()
        error = obj.get_mime_type(extension)
        assert error['message'] == "Unsupported file extension."
