from src.scrapper.oliveyoung import (
    get_oliveyoung_category_urls,
    get_brand_in_each_category,
    generate_query_keyword,
    get_brand_shop_url
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


@pytest.mark.skip(reason="tested")
def test_generate_query_keyword():
    brand_dict = get_brand_in_each_category(category_url)
    brand_dict = generate_query_keyword(brand_dict)
    assert brand_dict is not None


@pytest.mark.skip(reason="tested")
def test_generate_brand_shop_url():    
    brand_dict = get_brand_shop_url(
        generate_query_keyword(
            get_brand_in_each_category(category_url)
        )
    )
    assert brand_dict is not None


def test_get_items():
    from src.scrapper import get_soup

    url = 'https://www.oliveyoung.co.kr/store/display/getBrandShopDetail.do?onlBrndCd=A000517'
    brand_url_soup = get_soup(url)
    div_tag = brand_url_soup.find_all('div', class_='prod-info')
    for div in div_tag:
        item_name = div.find('a').get('data-attr')
        is_in_promotion = div.find('div', class_="discount") is not None
        print(item_name, is_in_promotion)
    