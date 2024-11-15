from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import time
import random

from src.scrapper.models import brand_generator

class Items:
    def __init__(self):
        pass

    def crawl_items(self):
        self._get_items()

    def _get_items(self) -> None:
        """
        각 브랜드의 제품 정보 추가 - 제품ID, 제품명, url, 프로모션여부
        """
        for brand in self.brand_metadata.keys():
            brand_url = self.brand_metadata[brand].brand_shop_detail_url
            driver = webdriver.Chrome()
            driver.get(brand_url)

            # 1페이지 상품 정보 수집
            self._get_products(driver, brand)

            # 다음 페이지 버튼 찾기
            next_pages = driver.find_elements(By.CSS_SELECTOR, '.pageing a[data-page-no]')
            if next_pages:
                for next_page in next_pages:
                    try:
                        driver.execute_script("arguments[0].click();", next_page)
                        time.sleep(random.randrange(5, 10) + random.random())  # 페이지 로딩 대기
                        response = requests.get(brand_url)
                        if response.status_code != 200:
                            time.sleep(10)
                    except:
                        time.sleep(10)

                    self._get_products(driver, brand)

    def _get_products(self, driver, brand) -> None:
        """
        하나의 brand page의 item page x에 있는 아이템정보(id, url, 상품명, 할인여부) 수집
        """
        products = driver.find_elements(By.CSS_SELECTOR, 'ul.prod-list.goodsProd div.prod a.thumb')
        for product in products:
            href = product.get_attribute('href')
            data_ref_goodsno = product.get_attribute('data-ref-goodsno')
            data_attr = product.get_attribute('data-attr')
            is_in_promotion = len(product.find_elements(By.CLASS_NAME, 'discount')) > 0
            self.brand_metadata[brand].items[data_ref_goodsno] = {
                'item_name': data_attr,
                'href': href,
                'is_in_promotion': is_in_promotion
            }
