from urllib.request import urlopen
from bs4 import BeautifulSoup


def get_soup(url: str = None):
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    return soup