from selenium import webdriver
from selenium.webdriver.common.by import By
from collections import defaultdict
import requests
import time
import random

from src.scrapper.models import oliveyoung_item_generator

class Items:
    def __init__(self, brand_name: str, brand_url: str):
        self.brand = brand_name
        self.brand_url = brand_url
        self.data = defaultdict(oliveyoung_item_generator)
        self.driver = webdriver.Chrome()

    def crawl_items(self):
        self._get_items()

    def _get_items(self) -> None:
        """
        하나의 brand page의 item page x에 있는 아이템정보(id, url, 상품명, 할인여부) 수집
        """
        self.driver.get(self.brand_url)

        # 1페이지 상품 정보 수집
        self._get_products()

        # 다음 페이지 버튼 찾기
        next_pages = self.driver.find_elements(By.CSS_SELECTOR, '.pageing a[data-page-no]')
        if next_pages:
            for next_page in next_pages:
                try:
                    self.driver.execute_script("arguments[0].click();", next_page)
                    time.sleep(random.randrange(5, 10) + random.random())  # 페이지 로딩 대기
                    response = requests.get(self.brand_url)
                    if response.status_code != 200:
                        time.sleep(10)
                except:
                    time.sleep(10)

                self._get_products()

    def _get_products(self) -> None:
        products = self.driver.find_elements(By.CSS_SELECTOR, 'ul.prod-list.goodsProd div.prod a.thumb')
        for product in products:
            href = product.get_attribute('href')
            data_ref_goodsno = product.get_attribute('data-ref-goodsno')
            data_attr = product.get_attribute('data-attr')
            is_in_promotion = len(product.find_elements(By.CLASS_NAME, 'discount')) > 
            item_id = f"{self.brand}_{data_ref_goodsno}"

            self.data[item_id].item_name = data_attr
            self.data[item_id].item_detail_url = href
            self.data[item_id].is_in_promotion = is_in_promotion
