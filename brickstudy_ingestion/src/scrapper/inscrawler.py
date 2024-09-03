import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
from collections import defaultdict

from src.scrapper.models import inst_generator


class InsCrawler:
    def __init__(self, keywords: list = None, dev: bool = False):
        if dev:
            proj_path = f'{'/'.join(os.getcwd().split('/')[:os.getcwd().split('/').index('brickstudy_ingestion')])}/brickstudy_ingestion'
        else:
            proj_path = '/opt/airflow/brickstudy_ingestion'
        self.base_path = f'{proj_path}/src/scrapper'

        self.user_id, self.password = self.load_config(dev=dev)
        self.keywords = keywords
        self.data = defaultdict(inst_generator)
        self.driver = webdriver.Chrome()
        self.login()

    def load_config(self, dev: bool = False):
        if dev:
            with open(f'{self.base_path}/config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)

            username = config['login']['username']
            password = config['login']['password']
        else:
            username = os.environ('INSTAGRAM_ID')
            password = os.environ('INSTAGRAM_PASSWORD')
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
        time.sleep(80)

    def materialize(self):
        """
        self.data to csv file
        """
        from src.scrapper.utils import current_datetime_getter
        import csv

        with open(f"{self.base_path}/insdata_{current_datetime_getter()}.csv", 'w') as f:
            w = csv.writer(f)
            w.writerow(self.data.values())