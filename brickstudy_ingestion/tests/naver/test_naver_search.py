import os
import pytest
import requests
from dotenv import load_dotenv

from src.naver.naver_search import NaverSearch
from src.common.exception import ExtractError
from src.common.errorcode import Naver

# .env 파일 로드
load_dotenv()

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
    client_id = "wrong_id_123"
    client_secret = os.getenv('NAVER_API_CLIENT_SECERT')

    # when : Naver news api 요청
    # then : errorcode
    with pytest.raises(ExtractError):
        client = NaverSearch(PLATFROM, RESPONSE_FORMAT)
        client.headers = {
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret
        }
        result = client.request_with_keword(QUERY, DISPLAY, START, SORT)

        assert result["message"] == Naver.AuthError.value["message"]
        # assert result["log"]["errorMessage"] == 'NID AUTH Result Invalid (1000) : Authentication failed. (인증에 실패했습니다.)'
        # assert result["log"]["errorCode"] == '024'


def test_naver_search_cannot_connect_client_with_invalid_secret_key():
    # given : 잘못된 네이버 ID
    client_id = os.getenv('NAVER_API_CLIENT_ID')
    client_secret = "wrong_secret"

    # when : Naver news api 요청
    # then : errorcode
    with pytest.raises(ExtractError):
        client = NaverSearch(PLATFROM, RESPONSE_FORMAT)
        client.headers = {
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret
        }
        result = client.request_with_keword(QUERY, DISPLAY, START, SORT)

        assert result["message"] == Naver.AuthError.value["message"]
        # assert result["log"]["errorMessage"] == 'NID AUTH Result Invalid (28) : Authentication failed. (인증에 실패했습니다.)'
        # assert result["log"]["errorCode"] == '024'
