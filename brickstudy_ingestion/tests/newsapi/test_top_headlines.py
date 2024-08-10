import pytest
import json

from src.newsapi.top_headlines import TopHeadline
from src.common.exception import ExtractError


# Mock
COUNTRY = "kr"
CATEGORY = "business" # business, entertainment, general, health, science, sports, technology


def test_can_request_new_contents():
    # given : 유효한 key
    # when : api 요청
    result = TopHeadline(COUNTRY, CATEGORY).request_with_country_category()
    result = json.loads(result)
    # 20개씩만 수집 가능

    # then : 응답 확인
    assert result["status"] == "ok"
    assert result["totalResults"] > 0


def test_cannot_requrest_new_contents_with_wrong_key():
    # given : 유효하지 않은 Key(횟수 만료?)

    WRONG_API_KEY = "wrong12314sdfgdagfa"
    client = TopHeadline(COUNTRY, CATEGORY)
    client.base_url = f"https://newsapi.org/v2/top-headlines?apiKey={WRONG_API_KEY}"

    # when : api 요청
    # then : 오류
    with pytest.raises(ExtractError):
        client.request_with_country_category()
