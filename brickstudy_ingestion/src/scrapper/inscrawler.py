import os
import time
import json
from collections import defaultdict
import random

from src.scrapper.models import inst_generator
from src.scrapper.utils import get_driver


class InsCrawler:
    def __init__(self,
                 keywords: list = None,
                 dev: bool = False,
                 driver=None):
        self.account_x = random.randrange(0, 2)
        if dev:
            proj_path = f"{'/'.join(os.getcwd().split('/')[:os.getcwd().split('/').index('ETL') + 1])}/brickstudy_ingestion"
            self.driver = get_driver()
        else:
            proj_path = '/opt/airflow/brickstudy_ingestion'
            self.driver = driver
        self.base_path = f"{proj_path}/src/scrapper"

        user_id, password = self.load_config(dev=dev)
        self.keywords = keywords
        self.data = defaultdict(inst_generator)
        self.numof_error = 0

        self.login(user_id, password)

        if self.suspicous_check():
            #TODO 계정 사용비율 낮추기
            print("return True in suspicious check")
            time.sleep(300)


    def load_config(self, dev: bool = False):
        if dev:
            with open(f'{self.base_path}/config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)

            username = config['login']['username'][self.account_x]
            password = config['login']['password'][self.account_x]
        else:
            username = os.getenv('INSTAGRAM_CLIENT_ID')
            password = os.getenv('INSTAGRAM_CLIENT_PASSWORD')
        return (username, password)

    def login(self, user_id: str, password: str):
        # Instagram 접속 및 로그인
        url = 'https://www.instagram.com/'
        self.driver.get(url)
        time.sleep(random.randrange(4, 6) + random.random())
        self.driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(user_id)
        time.sleep(random.randrange(1, 3) + random.random())
        self.driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(password)
        time.sleep(random.randrange(1, 3) + random.random())
        self.driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div').click()
        time.sleep(random.randrange(5, 11) + random.random())

    def materialize(self):
        """
        self.data to csv file
        """
        from src.scrapper.utils import current_datetime_getter
        import csv

        with open(f"{self.base_path}/results/insdata_{current_datetime_getter()}.csv", 'w') as f:
            w = csv.writer(f)
            w.writerow(self.data.values())

    def suspicous_check(self):
        """ 현재 자동화 행동 의심받는지 확인 """
        try:
            if 'wbloks_1' in self.driver.page_source:
                print("자동화된 활동 경고가 나타났습니다.")

                close_button = self.driver.find_element(By.XPATH, '//div[@aria-label="Dismiss"]')
                self.driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}));", close_button)

                # # 닫기 버튼 클릭, 계정 사용 일시 중지
                # close_button = WebDriverWait(self.driver, 5).until(
                #     EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Dismiss"]'))
                # )
                # close_button.click()
                return True
            return False
        except Exception:
            self.numof_error += 1
            return False

