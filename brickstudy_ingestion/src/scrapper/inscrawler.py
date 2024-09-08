import os
import time
import json
from collections import defaultdict
import random
from selenium import webdriver
from selenium.webdriver.common.by import By

from src.scrapper.models import inst_generator


class InsCrawler:
    def __init__(self,
                 keywords: list = None,
                 dev: bool = False,
                 driver=None):
        if dev:
            proj_path = f"{'/'.join(os.getcwd().split('/')[:os.getcwd().split('/').index('ETL') + 1])}/brickstudy_ingestion"
            self.driver = self.make_driver()
        else:
            proj_path = '/opt/airflow/brickstudy_ingestion'
            self.driver = driver

        self.base_path = f"{proj_path}/src/scrapper"
        self.user_id, self.password = self.load_config(dev=dev)
        self.keywords = keywords
        self.data = defaultdict(inst_generator)
        self.numof_error = 0

        self.login()

    @staticmethod
    def make_driver():
        user_agent_lst = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
        ]
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        options.add_experimental_option("useAutomationExtension", False)
        driver = webdriver.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": user_agent_lst[0]})
        return driver

    def load_config(self, dev: bool = False):
        if dev:
            with open(f'{self.base_path}/config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)

            x = random.randrange(0, 2)
            username = config['login']['username'][x]
            password = config['login']['password'][x]
        else:
            username = os.getenv('INSTAGRAM_CLIENT_ID')
            password = os.getenv('INSTAGRAM_CLIENT_PASSWORD')
        return (username, password)

    def login(self):
        # Instagram 접속 및 로그인
        url = 'https://www.instagram.com/'
        self.driver.get(url)
        time.sleep(random.randrange(4, 6))
        user = self.driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')
        user.send_keys(self.user_id)
        self.driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(self.password)
        self.driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div').click()
        time.sleep(random.randrange(5, 11))

    def materialize(self):
        """
        self.data to csv file
        """
        from src.scrapper.utils import current_datetime_getter
        import csv

        with open(f"{self.base_path}/results/insdata_{current_datetime_getter()}.csv", 'w') as f:
            w = csv.writer(f)
            w.writerow(self.data.values())