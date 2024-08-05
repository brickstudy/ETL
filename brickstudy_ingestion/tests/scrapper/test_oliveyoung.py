from src.scrapper.oliveyoung import (
    get_oliveyoung_category_urls,
    get_brand_in_each_category
)
import pytest


category_url = [('공통^드로우^스킨케어_스킨/토너', '100000100010013')]


@pytest.mark.skip(reason="tested")
def test_get_oliveyoung_category_urls():
    # category_urls 받아오기
    category_urls = get_oliveyoung_category_urls()
    assert category_urls is not None


@pytest.mark.skip(reason="tested")
def test_get_brand_in_each_category():
    brand_info = get_brand_in_each_category(category_url)
    assert brand_info is not None


def test_generate_query_keyword():
    import googletrans

    brand_dict = get_brand_in_each_category(category_url)
    translator = googletrans.Translator()
    translator.raise_Exception = True

    for brand in brand_dict.keys():
        eng_brand = translator.translate(brand, dest="en", src='auto').text
        brand_dict[brand].query_keyword = [brand, eng_brand]

    assert brand_dict is not None
