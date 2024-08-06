from collections import defaultdict

from . import get_soup
from src.scrapper.models import brand_generator


class Brand:
    def __init__(self, brand_metadata=None) -> None:
        if brand_metadata:
            self.brand_metadata = brand_metadata
        else:
            self.brand_metadata = defaultdict(brand_generator)

    def crawl_brand_metadata(self):
        self._get_brand_in_each_category(
            self._get_oliveyoung_category_urls()
        )
        self._get_brand_shop_url()

    def crawl_items(self):
        self._get_items()

    @staticmethod
    def _get_oliveyoung_category_urls() -> list:
        """
        올리브영 랜딩페이지의 카테고리레이어 에서 각 카테고리의 dispCatNo 값 파싱
        | return | (category 이름, url id) 를 원소로 갖는 리스트
        """
        url = 'https://www.oliveyoung.co.kr/store/display/getCategoryShop.do?dispCatNo=10000010002&gateCd=Drawer&t_page=%EB%93%9C%EB%A1%9C%EC%9A%B0_%EC%B9%B4%ED%85%8C%EA%B3%A0%EB%A6%AC&t_click=%EC%B9%B4%ED%85%8C%EA%B3%A0%EB%A6%AC%ED%83%AD_%EB%8C%80%EC%B9%B4%ED%85%8C%EA%B3%A0%EB%A6%AC&t_1st_category_type=%EB%8C%80_%EB%A9%94%EC%9D%B4%ED%81%AC%EC%97%85'
        soup = get_soup(url)
        assert soup is not None

        category_urls = []
        for a_tag in soup.find_all('a'):
            href = a_tag.get('href')
            if href and "javascript:common.link.moveCategory" in href:
                data_attr = a_tag.get('data-attr')
                data_ref_dispcatno = a_tag.get('data-ref-dispcatno')
                if data_attr is not None and data_ref_dispcatno is not None:
                    category_urls.append((data_attr, data_ref_dispcatno))
        return category_urls

    def _get_brand_in_each_category(self, category_urls: list) -> None:
        """
        파싱한 dispCatNo 기준으로 url 접근해서 해당 카테고리 내 브랜드 정보 파싱
        """
        base_url = 'https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo='

        for category_name, category_id in category_urls:
            cat_name = category_name.split('^')[-1]  # 공통^드로우^향수/디퓨저_여성향수
            soup = get_soup(base_url + category_id)
            # 모든 input 태그 찾기
            input_tags = soup.find_all('input', {'type': 'checkbox'})
            # data-brndnm 속성값 추출
            brand_names = [input_tag.get('data-brndnm') for input_tag in input_tags]
            for brand in brand_names:
                self.brand_metadata[brand].category.append(cat_name)

    def _generate_query_keyword(self) -> None:
        """
        구글번역 라이브러리 사용하여 브랜드 이름 영문으로 번역하여 query_keyword 추가
        """
        import googletrans

        translator = googletrans.Translator()
        translator.raise_Exception = True

        for brand in self.brand_metadata.keys():
            eng_brand = translator.translate(brand, dest="en", src='auto').text
            self.brand_metadata[brand].query_keyword = [brand, eng_brand]

    def _get_brand_shop_url(self) -> None:
        """
        각 브랜드의 올리브영 브랜드페이지 url 추가
        query_keyword에 올리브영에서 태깅한 영문 변환 브랜드명 추가
        """
        total_brand_list_soup = get_soup("https://www.oliveyoung.co.kr/store/main/getBrandList.do")
        brand_base_url = "https://www.oliveyoung.co.kr/store/display/getBrandShopDetail.do?onlBrndCd="
        code_name = {}

        for a_tag in total_brand_list_soup.find_all('a'):
            brand_code = a_tag.get('data-ref-onlbrndcd')
            if brand_code:
                brand_name = a_tag.text
                if brand_name in self.brand_metadata.keys():  # Kor brand name
                    self.brand_metadata[brand_name].brand_shop_detail_url = brand_base_url + brand_code
                    code_name[brand_code] = brand_name
                else:                                # Eng brand name
                    try:
                        kor_brand_name = code_name[brand_code]
                        self.brand_metadata[kor_brand_name].query_keyword.append(brand_name)
                    except Exception:
                        pass

    def _get_items(self) -> None:
        """
        각 브랜드의 제품 리스트, 해당 제품의 프로모션 여부 추가
        """
        for brand in self.brand_metadata.keys():
            brand_url = self.brand_metadata[brand].brand_shop_detail_url
            brand_url_soup = get_soup(brand_url)
            if brand_url_soup is None:
                continue
            item_dic = {}
            for div in brand_url_soup.find_all('div', class_='prod-info'):
                item_name = div.find('a').get('data-attr')
                is_in_promotion = div.find('div', class_="discount") is not None
                item_dic[item_name] = is_in_promotion
            self.brand_metadata[brand].items = item_dic
