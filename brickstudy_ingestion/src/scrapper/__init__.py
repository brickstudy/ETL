import urllib
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import random
import time

from src.common.exception import ExtractError


def get_soup(url: str = None):
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
