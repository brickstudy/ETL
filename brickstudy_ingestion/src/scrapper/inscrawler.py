import os
import time
import json
from collections import defaultdict
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.scrapper.models import inst_generator


class InsCrawler:
    def __init__(self,
                 keywords: list = None,
                 dev: bool = False,
                 driver=None):
        self.account_x = random.randrange(0, 2)
        if dev:
            proj_path = f"{'/'.join(os.getcwd().split('/')[:os.getcwd().split('/').index('ETL') + 1])}/brickstudy_ingestion"
            self.driver = self.make_driver()
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
            time.sleep()

    def make_driver(self):
        proxies = [
            ["211.223.89.176:51147",
            "121.66.105.19:51080",
            "121.66.105.19:51080",
            "8.213.128.6:8080"],
            ["8.213.129.20:8090",
            "8.213.129.20:5566",
            "8.213.137.155:8090",
            "8.220.204.215:808"],
            ["8.220.205.172:9098",
            "211.223.89.176:51147",
            "8.213.128.90:2019",
            "8.213.128.90:444"]
        ]
        user_agent_lst = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1636.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
        ]
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        proxy = proxies[self.account_x][random.randrange(0, 4)]
        print(proxy)
        webdriver.DesiredCapabilities.CHROME['proxy'] = {
            "socksProxy": proxy,
            "socksVersion": 4,
        }

        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        options.add_experimental_option("useAutomationExtension", False)
        driver = webdriver.Chrome(
            options=options
        )
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": user_agent_lst[self.account_x]})
        return driver

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


if __name__ == "__main__":
    test = InsCrawler(keywords='엔하이픈', dev=True)