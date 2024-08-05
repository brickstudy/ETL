from dataclasses import dataclass


@dataclass
class OliveyoungBrand:
    query_keyword: list                 # api 쿼리 키워드 - 브랜드 영문이름 등
    brand_shop_detail_url: str          # 브랜드관 url
    item_list: list                     # 브랜드 제품 리스트
    category: list                      # 브랜드가 속한 카테고리
    is_on_promotion: bool               # 할인 여부
    released_date: str = '2024/08/05'   # 신제품 출시 일자


def brand_generator():
    return OliveyoungBrand([], '', [], [], False, '')