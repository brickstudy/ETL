import os
import requests
from dotenv import load_dotenv


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
    client_id = os.getenv('NAVER_API_CLIENT_ID')
    client_secret = os.getenv('NAVER_API_CLIENT_SECERT')

    # when : Naver news api 요청
    base_url = f"https://openapi.naver.com/v1/search/{PLATFROM}.{RESPONSE_FORMAT}"
    sub_url = f"?query={QUERY}&display={DISPLAY}&start={START}&sort={SORT}"
    url = base_url + sub_url
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }

    response = requests.get(url, headers=headers)

    # then : json 데이터 확인
    assert response.status_code == 200

    data = response.json()
    assert data["start"] == 1
    assert data["display"] == 10
    assert data["items"]
    assert data["items"][0]["title"]
    assert data["items"][0]["originallink"]
    assert data["items"][0]["link"]
    assert data["items"][0]["description"]
    assert data["items"][0]["pubDate"]


def test_naver_search_cannot_connect_client_with_invalid_id():
    # given : 잘못된 네이버 ID
    client_id = "wrong_id_123"
    client_secret = os.getenv('NAVER_API_CLIENT_SECERT')

    # when : Naver news api 요청
    base_url = f"https://openapi.naver.com/v1/search/{PLATFROM}.{RESPONSE_FORMAT}"
    sub_url = f"?query={QUERY}&display={DISPLAY}&start={START}&sort={SORT}"
    url = base_url + sub_url
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }

    response = requests.get(url, headers=headers)

    # then : errorcode
    assert response.status_code == 401

    # data = response.json()
    # assert data["errorMessage"] == 'NID AUTH Result Invalid (1000) : Authentication failed. (인증에 실패했습니다.)'
    # assert data["errorCode"] == '024'


def test_naver_search_cannot_connect_client_with_invalid_secret_key():
    # given : 잘못된 네이버 ID
    client_id = os.getenv('NAVER_API_CLIENT_ID')
    client_secret = "wrong_secret"

    # when : Naver news api 요청
    base_url = f"https://openapi.naver.com/v1/search/{PLATFROM}.{RESPONSE_FORMAT}"
    sub_url = f"?query={QUERY}&display={DISPLAY}&start={START}&sort={SORT}"
    url = base_url + sub_url
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }

    response = requests.get(url, headers=headers)

    # then : errorcode
    assert response.status_code == 401

    # data = response.json()
    # assert data["errorMessage"] == 'NID AUTH Result Invalid (28) : Authentication failed. (인증에 실패했습니다.)'
    # assert data["errorCode"] == '024'
