import os
import json
import requests
from dotenv import load_dotenv


load_dotenv()

# Mock
COUNTRY = "kr"
API_KEY = os.getenv("NEWSAPI_KEY")
CATEGORY = "business" # business, entertainment, general, health, science, sports, technology


def test_can_request_new_contents():
    # given : 유효한 key
    base_url = f"https://newsapi.org/v2/top-headlines?country={COUNTRY}&category={CATEGORY}&apiKey={API_KEY}"

    # when : api 요청
    response = requests.get(base_url)
    result = response.json()    # 20개씩만 수집 가능

    # then : 응답 확인
    assert response.status_code == 200
    assert result["status"] == "ok"
    assert result["totalResults"] > 0


def test_cannot_requrest_new_contents_with_wrong_key():
    # given : 유효하지 않은 Key(횟수 만료?)
    WRONG_API_KEY = "wrong12314sdfgdagfa"
    base_url = f"https://newsapi.org/v2/top-headlines?country={COUNTRY}&category={CATEGORY}&apiKey={WRONG_API_KEY}"

    # when : api 요청
    response = requests.get(base_url)
    result = response.json()

    # then : 오류
    assert response.status_code == 401
    assert result["status"] == "error"
    assert result["code"] == "apiKeyInvalid"
