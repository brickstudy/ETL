import json
import pytest
from src.naver.naver_search import NaverSearch
from src.common.exception import ExtractError


# Mock
PLATFROM = "news"
RESPONSE_FORMAT = "json"
QUERY = "여행"  # 검색어. UTF-8로 인코딩되어야 합니다.
DISPLAY = 10    # 한 번에 표시할 검색 결과 개수(기본값: 10, 최댓값: 100)
START = 1   # 검색 시작 위치(기본값: 1, 최댓값: 1000)
SORT = "sim"    # 검색 결과 정렬 방법 - sim: 정확도순으로 내림차순 정렬(기본값) - date: 날짜순으로 내림차순 정렬


@pytest.fixture
def naver_api_client():
    return NaverSearch(
        target_platform=PLATFROM,
        resp_format=RESPONSE_FORMAT
    )


def test_nave_search_can_connect_client_with_valid(naver_api_client):
    # given : 유효한 네이버 ID, SECRET KEY
    # when : Naver news api 요청
    result = naver_api_client.request_with_keyword(QUERY, DISPLAY, START, SORT)
    result = json.loads(result)

    # then : json 데이터 확인
    assert result["start"] == 1
    assert result["display"] == 10
    assert result["items"]
    assert result["items"][0]["title"]
    assert result["items"][0]["originallink"]
    assert result["items"][0]["link"]
    assert result["items"][0]["description"]
    assert result["items"][0]["pubDate"]


def test_naver_search_cannot_connect_client_with_invalid_id(naver_api_client):
    # given : 잘못된 네이버 ID
    wrong_id = "wrong_id"

    # when : Naver news api 요청
    # then : errorcode
    with pytest.raises(ExtractError):
        naver_api_client.headers["X-Naver-Client-Id"] = wrong_id
        result = naver_api_client.request_with_keyword(QUERY, DISPLAY, START, SORT)

        assert result["message"] == Naver.AuthError.value["message"]
        # assert result["log"]["errorMessage"] == 'NID AUTH Result Invalid (1000) : Authentication failed. (인증에 실패했습니다.)'
        # assert result["log"]["errorCode"] == '024'


def test_naver_search_cannot_connect_client_with_invalid_secret_key(naver_api_client):
    # given : 잘못된 네이버 ID
    wrong_secret = "wrong_secret"

    # when : Naver news api 요청
    # then : errorcode
    with pytest.raises(ExtractError):
        naver_api_client.headers["X-Naver-Client-Secret"] = wrong_secret
        result = naver_api_client.request_with_keyword(QUERY, DISPLAY, START, SORT)

        assert result["message"] == Naver.AuthError.value["message"]
        # assert result["log"]["errorMessage"] == 'NID AUTH Result Invalid (28) : Authentication failed. (인증에 실패했습니다.)'
        # assert result["log"]["errorCode"] == '024'


def test_naver_search_exceed_daily_request_quota(naver_api_client):
    # given : 네이버 api request 할당량 초과 or 1초에 너무 많은 request
    # then : errorcode 429
    with pytest.raises(ExtractError):
        for _ in range(25000):
            result = naver_api_client.request_with_keyword(QUERY)
        assert result["message"] == Naver.LimitExceedError.value["message"]
