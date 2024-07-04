# 네이버 검색 API 예제 - 블로그 검색
import urllib.request
import logging

from brickstudy_ingestion.src.naver_api import NaverAPI

class Logger:
    def __init__(self, name: str) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        

class NaverSearchAPI(NaverAPI):
    def __init__(self, target_search_platform: str='news', respond_format: str='json') -> None:
        """
        : target_search_platform : 검색 대상 플랫폼(blog, news, cafe, etc)
        : respond_format         : api 응답 반환 포맷(json or xml)
        """
        super().__init__()
        self.url = f"https://openapi.naver.com/v1/search/{target_search_platform}.{respond_format}?query="
        self.log_instance = Logger(target_search_platform)

    def request_with_keyword(self, 
                             query: str, 
                             display: int=10,
                             start: int=1,
                             sort: str='sim'):
        assert 10<=display<=100 and 1<=start<=1000 and sort in ['sim', 'date']

        encText = urllib.parse.quote(query)
        url = self.url + encText + f'&display={str(display)}&start={str(start)}&sort={sort}'

        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",self.client_id)
        request.add_header("X-Naver-Client-Secret",self.client_secret)

        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            return response_body.decode('utf-8').items
        else:
            print("Error Code:" + rescode)
            return

if __name__ == '__main__':
    NewsAPI = NaverSearchAPI()
    NewsAPI.request_with_keyword('여행')

