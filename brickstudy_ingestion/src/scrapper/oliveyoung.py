from . import get_soup


def get_oliveyoung_category_urls() -> list:
    """
    올리브영 랜딩페이지의 카테고리레이어 에서 각 카테고리의 dispCatNo 값 파싱
    | return | (category 이름, url id) 를 원소로 갖는 리스트
    """
    url = 'https://www.oliveyoung.co.kr/store/main/main.do'
    soup = get_soup(url)

    category_urls = []
    for a_tag in soup.find_all('a'):
        href = a_tag.get('href')
        if href and "javascript:common.link.moveCategory" in href:
            data_attr = a_tag.get('data-attr')
            data_ref_dispcatno = a_tag.get('data-ref-dispcatno')
            category_urls.append((data_attr, data_ref_dispcatno))
    return category_urls


def get_brand_in_each_category(category_urls: list) -> dict:
    """
    파싱한 dispCatNo 기준으로 url 접근해서 해당 카테고리 내 브랜드 정보 파싱
    | return | {'brand_name': OliveyoungBrand_object} 구조 해시맵
    """
    from collections import defaultdict
    from src.scrapper.models import brand_generator

    base_url = 'https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo='
    brand_metadata = defaultdict(brand_generator)

    for category_name, category_id in category_urls:
        if category_name is None:
            continue

        cat_name = category_name.split('^')[-1]  # 공통^드로우^향수/디퓨저_여성향수
        soup = get_soup(base_url + category_id)
        # 모든 input 태그 찾기
        input_tags = soup.find_all('input', {'type': 'checkbox'})
        # data-brndnm 속성값 추출
        brand_names = [input_tag.get('data-brndnm') for input_tag in input_tags]
        for brand in brand_names:
            brand_metadata[brand].category.append(cat_name)
    return brand_metadata


def generate_query_keyword(brand_metadata: dict) -> dict:
    """
    구글번역 라이브러리 사용하여 브랜드 이름 영문으로 번역하여 query_keyword 추가
    | return | {'brand_name': OliveyoungBrand_object} 구조 해시맵
    """
    import googletrans

    translator = googletrans.Translator()
    translator.raise_Exception = True

    for brand in brand_metadata.keys():
        eng_brand = translator.translate(brand, dest="en", src='auto').text
        brand_metadata[brand].query_keyword = [brand, eng_brand]

    return brand_metadata


def get_brand_shop_url(brand_metadata: dict) -> dict:
    """
    각 브랜드의 올리브영 브랜드페이지 url 추가
    query_keyword에 올리브영에서 태깅한 영문 변환 브랜드명 추가
    | return | {'brand_name': OliveyoungBrand_object} 구조 해시맵
    """
    total_brand_list_soup = get_soup("https://www.oliveyoung.co.kr/store/main/getBrandList.do")
    brand_base_url = "https://www.oliveyoung.co.kr/store/display/getBrandShopDetail.do?onlBrndCd="
    code_name = {}

    for a_tag in total_brand_list_soup.find_all('a'):
        brand_code = a_tag.get('data-ref-onlbrndcd')
        if brand_code:
            brand_name = a_tag.text
            if brand_name in brand_metadata.keys():  # Kor brand name
                brand_metadata[brand_name].brand_shop_detail_url = brand_base_url + brand_code
                code_name[brand_code] = brand_name
            else:                                # Eng brand name
                try:
                    kor_brand_name = code_name[brand_code]
                    brand_metadata[kor_brand_name].query_keyword.append(brand_name)
                finally:
                    continue
    return brand_metadata
