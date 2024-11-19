def get_driver():
    """
    return selenium driver
    """
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
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


def get_soup(url: str = None):
    import urllib
    from urllib.request import urlopen
    from urllib.error import HTTPError, URLError
    from bs4 import BeautifulSoup
    import random
    import time

    from src.common.exception import ExtractError

    user_agent_lst = ['Googlebot', 'Yeti', 'Daumoa', 'Twitterbot']
    user_agent = user_agent_lst[random.randint(0, len(user_agent_lst) - 1)]
    headers = {'User-Agent': user_agent}

    try:
        req = urllib.request.Request(url, headers=headers)
        page = urlopen(req)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
    except (HTTPError, URLError) as e:
        err = ExtractError(
            code=000,
            message=f"**{url}** HTTPError/URLError. Sleep 5 and continue.",
            log=e
        )
        time.sleep(5)  # TODO 이 경우 해당 url에 대해 재실행 필요
    except (ValueError) as e:
        err = ExtractError(
            code=000,
            message=f"**{url}** ValueError. Ignore this url parameter.",
            log=e
        )
        print(err)
        soup = None  # TODO 해당 url 무시
    else:
        time.sleep(random.random())
        return soup


def dict_partitioner(data: dict, level: int):
    total_n = len(data)
    partition_n = total_n // level
    partition_remain = total_n % level

    brand_lst = list(data.keys())
    start = 0
    for i in range(level):
        end = start + partition_n + (1 if i < partition_remain else 0)
        part = {key: data[key] for key in brand_lst[start:end]}
        yield part
        start = end


def write_local_as_json(data: dict, file_path: str, file_name: str):
    """
    data : dictionary with the dataclass value
    file_path : directory string where the json file created
    file_name : file name without extension
    """
    from dataclasses import asdict
    import json
    import os

    try:
        os.makedirs(file_path, exist_ok=True)
    except PermissionError:
        print("*** write_local_as_json cannot create given directory ***")
        raise

    path = f"{file_path}/{file_name}.json"
    json_data = {b_name: asdict(details) for b_name, details in data.items()}
    with open(path, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)


def read_local_as_dict(file_path, file_name):
    import json
    from src.scrapper.models import OliveyoungBrand

    path = f"{file_path}/{file_name}.json"
    with open(path, 'r', encoding='utf-8') as json_file:
        loaded_data = json.load(json_file)

    for key, val in loaded_data.items():
        loaded_data[key] = OliveyoungBrand(**val)
    return loaded_data


def randmized_sleep(average=1):
    import random
    from time import sleep

    _min, _max = average * 1 / 2, average * 3 / 2
    sleep(random.uniform(_min, _max))


def retry(attempt=10, wait=0.3):
    from functools import wraps
    from time import sleep
    from src.common.exception import RetryException

    def wrap(func):
        @wraps(func)
        def wrapped_f(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except RetryException:
                if attempt > 1:
                    sleep(wait)
                    return retry(attempt - 1, wait)(func)(*args, **kwargs)
                else:
                    exc = RetryException()
                    exc.__cause__ = None
                    raise exc

        return wrapped_f

    return wrap


def current_datetime_getter():
    import pytz
    from datetime import datetime
    kst = pytz.timezone('Asia/Seoul')
    current_time = datetime.now(kst)
    current_datetime = current_time.strftime("%Y%m%d_%H%M%S")
    return current_datetime