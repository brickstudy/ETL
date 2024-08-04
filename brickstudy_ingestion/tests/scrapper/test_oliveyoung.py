from src.scrapper.oliveyoung import (
    get_oliveyoung_category_urls,
    get_brand_in_each_category
)

import json


def test_get_oliveyoung_category_urls():
    # category_urls 받아오기
    category_urls = get_oliveyoung_category_urls()
    assert category_urls is not None


def test_get_brand_in_each_category():
    brand_info = get_brand_in_each_category(get_oliveyoung_category_urls())
    assert brand_info is not None
    with open('./brand_info.json', 'w') as f:
        f.write(json.dumps(brand_info))
