import os

from src.common.exception import RetryException

from browser import Browser
from utils import retry


class InsCrawler():
    URL = "https://www.instagram.com"
    RETRY_LIMIT = 10

    def __init__(self, has_screen=False):
        super(InsCrawler, self).__init__()
        self.browser = Browser(has_screen)
        self.page_height = 0
        self.login()

    def login(self):
        browser = self.browser
        url = "%s/accounts/login/" % (InsCrawler.URL)
        browser.get(url)
        u_input = browser.find_one('input[name="username"]')
        u_input.send_keys(os.getenv('INSTAGRAM_ID'))
        p_input = browser.find_one('input[name="password"]')
        p_input.send_keys(os.getenv('INSTAGRAM_PWD'))

        login_btn = browser.find_one('button[type="submit"]')
        login_btn.click()

        @retry()
        def check_login():
            if browser.find_one('input[name="username"]'):
                raise RetryException()

        check_login()

    def get_latest_posts_by_tag(self, tag, num):
        tag = 'enhypen'
        url = f"{InsCrawler.URL}/explore/search/keyword/?q=%23{tag}"
        self.browser.get(url)
        self.browser.scroll_down()
        #TODO 게시물 클릭, 컨텐츠 가져오기