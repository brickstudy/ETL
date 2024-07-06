import requests
from . import client_id, client_secret
from src.common.exception import ExtractError
from src.common.errorcode import Naver


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
        try:
            sub_url = f"?query={query}&display={display}&start={start}&sort={sort}"
            url = self.base_url + sub_url

            response = requests.get(url, headers=self.headers)

            if response.status_code == 401:
                raise ExtractError(**Naver.AuthError.value,
                                   log=response.json())
            return response.json()
        except Exception as e:
            raise ExtractError(**Naver.UnknownError.value, log=str(e))
