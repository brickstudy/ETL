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


def write_local_as_json(data, file_path, file_name):
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