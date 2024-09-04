import os
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import json
from collections import defaultdict

from src.scrapper.models import inst_generator


class InsCrawler:
    def __init__(self,
                 keywords: list = None,
                 dev: bool = False,
                 driver: webdriver = None):
        if dev:
            proj_path = f"{'/'.join(os.getcwd().split('/')[:os.getcwd().split('/').index('ETL') + 1])}/brickstudy_ingestion"
        else:
            proj_path = '/opt/airflow/brickstudy_ingestion'
        self.base_path = f"{proj_path}/src/scrapper"

        self.user_id, self.password = self.load_config(dev=dev)
        self.keywords = keywords
        self.data = defaultdict(inst_generator)

        if driver is None:
            self.load_driver(dev)
            self.login()
        else:
            self.driver = driver
        
    def load_driver(self, dev: bool = False):
        if dev:
            self.driver = webdriver.Chrome()
        else:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            self.driver = webdriver.Chrome(
                executable_path=ChromeDriverManager().install(),
                options=options
            )

    def load_config(self, dev: bool = False):
        if dev:
            with open(f'{self.base_path}/config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)

            username = config['login']['username']
            password = config['login']['password']
        else:
            username = os.getenv('INSTAGRAM_CLIENT_ID')
            password = os.getenv('INSTAGRAM_CLIENT_PASSWORD')
        return (username, password)

    def login(self):
        # Instagram 접속 및 로그인
        url = 'https://www.instagram.com/'
        self.driver.get(url)
        time.sleep(6)
        user = self.driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')
        user.send_keys(self.user_id)
        self.driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(self.password)
        self.driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div').click()
        time.sleep(40)

    def materialize(self):
        """
        self.data to csv file
        """
        from src.scrapper.utils import current_datetime_getter
        import csv

        with open(f"{self.base_path}/results/insdata_{current_datetime_getter()}.csv", 'w') as f:
            w = csv.writer(f)
            w.writerow(self.data.values())