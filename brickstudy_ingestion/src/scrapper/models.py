from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class OliveyoungBrand:
    query_keyword: List[str]            # api 쿼리 키워드 - 브랜드 영문이름 등
    brand_shop_detail_url: str          # 브랜드관 url
    items: Dict[str, bool]              # 브랜드 제품 리스트 {제품명:할인여부}
    category: List[str]                 # 브랜드가 속한 카테고리
    released_date: str = field(default_factory='2024/08/05')   # 신제품 출시 일자


def brand_generator():
    return OliveyoungBrand(
        [],
        '',
        {},
        [],
        ''
    )


@dataclass
class InstagramData:
    brand: str
    post_url: str
    full_text: str
    username: str
    like: int
    saved_imgs: str
    date: str


def inst_generator():
    return InstagramData(
        '', '', '', '', 0, '', ''
    )
