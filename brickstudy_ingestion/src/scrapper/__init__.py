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
        page = urlopen(url, headers=headers)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
    except (HTTPError, URLError) as e:
        ExtractError(
            code=000,
            message=f"**{url}** open error",
            log=e
        )
        time.sleep(5)
    else:
        time.sleep(random.randrange(0, 3))
        return soup
