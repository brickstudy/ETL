import requests
from . import client_id, client_secret


class NaverSearch:
    def __init__(
            self,
            target_platform: str,
            resp_format: str = "json"
    ) -> None:
        self.base_url = f"https://openapi.naver.com/v1/search/{target_platform}.{resp_format}"
        self.headers = {
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret
        }

    def request_with_keword(
            self,
            query: str,
            display: int = 1,
            start: int = 1,
            sort: str = "sim"
    ) -> dict:
        sub_url = f"?query={query}&display={display}&start={start}&sort={sort}"
        url = self.base_url + sub_url

        response = requests.get(url, headers=self.headers)

        return response
