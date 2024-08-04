from . import get_soup


def get_oliveyoung_category_urls() -> list:
    """
    올리브영 랜딩페이지의 카테고리레이어 에서 각 카테고리의 dispCatNo 값 파싱
    | return | (category 이름, url id) 를 원소로 갖는 리스트
    """
    url = 'https://www.oliveyoung.co.kr/store/main/main.do?oy=0&t_page=%EC%8A%A4%ED%82%A8%EC%BC%80%EC%96%B4%20&gt;%20%EC%97%90%EC%84%BC%EC%8A%A4/%EC%84%B8%EB%9F%BC/%EC%95%B0%ED%94%8C&t_click=%ED%97%A4%EB%8D%94&t_header_type=%EB%A1%9C%EA%B3%A0'
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
    | return | {brand_name: [tags]} 꼴 해시맵
    """
    from collections import defaultdict

    base_url = 'https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo='
    brand_metadata = defaultdict(list)

    for category_name, category_id in category_urls:
        if category_name is None:
            continue

        category = category_name.split('^')[-1]  # 공통^드로우^향수/디퓨저_여성향수
        soup = get_soup(base_url + category_id)
        # 모든 input 태그 찾기
        input_tags = soup.find_all('input', {'type': 'checkbox'})
        # data-brndnm 속성값 추출
        brand_names = [input_tag.get('data-brndnm') for input_tag in input_tags]
        for brand in brand_names:
            brand_metadata[brand].append(category)
    return brand_metadata
