import os
import json
import requests


from src.common.exception import ExtractError
from src.common.errorcode import NewsApi


class TopHeadline:
    def __init__(self,
                 country: str = "kr",
                 category: str = "business"
                 ) -> None:
        API_KEY = os.getenv("NEWSAPI_CLIENT_ID")
        self.country = country
        self.category = category    # business, entertainment, general, health, science, sports, technology
        self.base_url = f"https://newsapi.org/v2/top-headlines?apiKey={API_KEY}"

    def request_with_country_category(self):
        print(os.getenv("NEWS_API_CLIENT_ID"))
        print(f"==========={self.base_url}")
        try:
            sub_url = f"&country={self.country}&category={self.category}"
            url = self.base_url + sub_url

            response = requests.get(url)
            content = response.json()

            if response.status_code == 401:
                raise ExtractError(**NewsApi.AuthError.value, log=str(content))

            return json.dumps(content, ensure_ascii=False)
        except Exception as e:
            raise ExtractError(**NewsApi.UnknownError.value, log=str(e))
