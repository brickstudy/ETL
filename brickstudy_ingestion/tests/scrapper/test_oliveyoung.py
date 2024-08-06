from src.scrapper.oliveyoung import Brand


brand_obj = Brand()
test_category_url = [('공통^드로우^스킨케어_스킨/토너', '100000100010013')]
test_brand = '구달'


def test_get_oliveyoung_category_urls():
    # category_urls 받아오기
    category_urls = brand_obj._get_oliveyoung_category_urls()
    assert len(category_urls)


def test_get_brand_in_each_category():
    brand_obj._get_brand_in_each_category(test_category_url)
    res = brand_obj.brand_metadata[test_brand].category
    print(res)
    assert len(res)


def test_generate_brand_shop_url():    
    brand_obj._get_brand_shop_url()
    res1 = brand_obj.brand_metadata[test_brand].query_keyword
    res2 = brand_obj.brand_metadata[test_brand].brand_shop_detail_url
    assert len(res1)
    assert res2

