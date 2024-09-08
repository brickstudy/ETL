import time
from bs4 import BeautifulSoup
import urllib
import re

from src.scrapper.inscrawler import InsCrawler


class InsURLCrawler(InsCrawler):
    def __init__(self, keywords: list = None, dev: bool = False):
        super().__init__(keywords, dev)

    def get_urls(self, keyword: str = None):
        if keyword is not None:              # execute with given keyword
            self._fetch_url_data(keyword)
        else:                                # execute with entire keywords
            for keyword in self.keywords:
                self._fetch_url_data(keyword)

    def _fetch_url_data(self, keyword):
        word = urllib.parse.quote(keyword)
        word_url = f'https://www.instagram.com/explore/tags/{word}/'
        self.driver.get(word_url)

        try:
            time.sleep(5)
            js = 'window.scrollBy(0,1000)'
            self.driver.execute_script(js)
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'lxml')

            divimg = soup.find_all('img', {'class': 'x5yr21d xu96u03 x10l6tqk x13vifvy x87ps6o xh8yej3'})
            if not divimg:
                print('이미지를 찾을 수 없습니다.')
                raise Exception

            for div in divimg:
                content = div.get('alt')
                if not content:
                    print('내용이 없습니다.')
                    continue

                a = div.find_parent('a')
                if a is None:
                    print('게시물 링크가 잘못되었습니다.')
                    continue
                urlto = a.get('href')
                if urlto is None:
                    print('게시물 링크가 없습니다.')
                    continue
                totalurl = 'https://www.instagram.com' + urlto
                self.data[urlto].brand = keyword
                self.data[urlto].post_url = totalurl

                modified_content = re.sub(r'\s*\n\s*', ' ', content)
                self.data[urlto].full_text = modified_content

            print(f'페이지 {keyword}에서 데이터를 가져오는 중...')
            time.sleep(5)

        except Exception as e:
            self.numof_error += 1
            print(e)
            print('오류 발생')

        print(f'키워드 {keyword}의 URL 정보 수집 완료.')