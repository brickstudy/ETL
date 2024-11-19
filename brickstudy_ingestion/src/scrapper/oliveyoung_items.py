from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime, timedelta
from collections import defaultdict
import requests
import time
import random

from src.scrapper.models import oliveyoung_item_generator
from src.scrapper.utils import write_local_as_json

class Items:
    def __init__(self, brand_name: str, brand_url: str):
        self.brand = brand_name
        self.brand_url = brand_url
        self.data = defaultdict(oliveyoung_item_generator)
        self.item_id = None
        self.driver = webdriver.Chrome()

    def crawl_items(self):
        # brand 페이지에서 전체 item 정보들 수집
        self.driver.get(self.brand_url)
        self._get_items()

        # 각 item 페이지에서 리뷰 수집
        for item_id in self.data.keys():
            self.item_id = item_id
            self.driver.get(self.data[item_id].item_detail_url)
            self._get_reviews()

    def _get_items(self) -> None:
        """
        하나의 brand page의 item page x에 있는 아이템정보(id, url, 상품명, 할인여부) 수집
        """
        # 최초 1페이지 상품 정보 수집
        self._get_products()
        # 페이지 넘기면서 상품 정보 수집
        next_pages = self.driver.find_elements(By.CSS_SELECTOR, '.pageing a[data-page-no]')
        if next_pages:
            for next_page in next_pages:
                try:
                    self.driver.execute_script("arguments[0].click();", next_page)
                    time.sleep(random.randrange(5, 10) + random.random())
                    response = requests.get(self.brand_url)
                    if response.status_code != 200:
                        time.sleep(10)
                except:
                    time.sleep(10)
                self._get_products()

    def _get_products(self) -> None:
        """
        아이템 element 찾아서 실제 수집 동작
        """
        products = self.driver.find_elements(By.CSS_SELECTOR, 'ul.prod-list.goodsProd div.prod a.thumb')
        for product in products:
            href = product.get_attribute('href')
            data_ref_goodsno = product.get_attribute('data-ref-goodsno')
            data_attr = product.get_attribute('data-attr')
            is_in_promotion = len(product.find_elements(By.CLASS_NAME, 'discount')) > 0
            item_id = f"{self.brand}_{data_ref_goodsno}"

            self.data[item_id].item_name = data_attr
            self.data[item_id].item_detail_url = href
            self.data[item_id].is_in_promotion = is_in_promotion

    def _get_reviews(self):
        self.__click_review_button()
        self.__click_latest_button()
        
        self.__get_reviews_with_page_moving()

    def __click_review_button(self) -> None:
        try:
            review_button_element = self.driver.find_element(By.CSS_SELECTOR, 'a.goods_reputation[data-attr="상품상세^상품상세_SortingTab^리뷰"]')
            self.driver.execute_script("arguments[0].scrollIntoView(true);", review_button_element)
            self.driver.execute_script("arguments[0].click();", review_button_element)
            time.sleep(random.randint(2, 4))
        except Exception as e:
            print(f"리뷰 버튼 클릭 실패: {e}")
    
    def __click_latest_button(self) -> None:
        try:
            latest_button_element = self.driver.find_element(By.CSS_SELECTOR, 'a[data-sort-type-code="latest"][data-attr="상품상세^리뷰정렬^최신순"]')
            self.driver.execute_script("arguments[0].scrollIntoView(true);", latest_button_element)
            self.driver.execute_script("arguments[0].click();", latest_button_element)
            time.sleep(random.randint(2, 4))
        except Exception as e:
            print(f"최신순 버튼 클릭 실패: {e}")

    def __get_reviews_with_page_moving(self):
        self.__get_reviews_in_each_page()
        next_pages = self.driver.find_elements(By.CSS_SELECTOR, '.pageing a[data-page-no]')
        flag = True
        while flag:
            flag = len(next_pages) == 10  # next page가 있으면 계속 클릭하면서 수집
            for i in range(len(next_pages)):
                try:
                    self.driver.execute_script("arguments[0].click();", next_pages[i])
                    time.sleep(random.randrange(5, 10) + random.random())
                except:
                    print("exception block in page moving")
                    time.sleep(3)
                self.__get_reviews_in_each_page()
                next_pages = self.driver.find_elements(By.CSS_SELECTOR, '.pageing a[data-page-no]')

    def __get_reviews_in_each_page(self):
        """
        리뷰 element 찾아서 실제 수집 동작
        """
        review_elements = self.driver.find_elements(By.CLASS_NAME, 'txt_inner')
        date_elements = self.driver.find_elements(By.CLASS_NAME, 'date')
        for rev_elem, date_elem in zip(review_elements, date_elements):
            self.data[self.item_id].reviews.append((rev_elem.text, date_elem.text))


if __name__ == "__main__":
    brand_name = "토리든"
    brand_url = "https://www.oliveyoung.co.kr/store/display/getBrandShopDetail.do?onlBrndCd=A002820&t_page=%EC%83%81%ED%92%88%EC%83%81%EC%84%B8&t_click=%EB%B8%8C%EB%9E%9C%EB%93%9C%EA%B4%80_%EC%83%81%EB%8B%A8&t_brand_name=%ED%86%A0%EB%A6%AC%EB%93%A0"
    item_x = Items(brand_name, brand_url)
    item_x.crawl_items()
    
    write_local_as_json(item_x.data, './', 'toridn')
