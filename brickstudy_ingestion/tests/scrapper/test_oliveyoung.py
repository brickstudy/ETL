from src.scrapper.oliveyoung import (
    get_oliveyoung_category_urls,
    get_brand_in_each_category,
    generate_query_keyword
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


def test_generate_brand_shop_url():
    from src.scrapper import get_soup
    
    brand_dict = generate_query_keyword(
        get_brand_in_each_category(category_url)
    )

    total_brand_list_soup = get_soup("https://www.oliveyoung.co.kr/store/main/getBrandList.do")
    brand_base_url = "https://www.oliveyoung.co.kr/store/display/getBrandShopDetail.do?onlBrndCd="
    code_name = {}
    for a_tag in total_brand_list_soup.find_all('a'):
        brand_code = a_tag.get('data-ref-onlbrndcd')
        if brand_code:
            brand_name = a_tag.text
            if brand_name in brand_dict.keys():  # Kor brand name
                brand_dict[brand_name].brand_shop_detail_url = brand_base_url + brand_code
                code_name[brand_code] = brand_name
            else:                                # Eng brand name
                try:
                    kor_brand_name = code_name[brand_code]
                    brand_dict[kor_brand_name].query_keyword.append(brand_name)
                finally:
                    continue
    print(brand_dict)