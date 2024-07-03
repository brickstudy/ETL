import os

class NaverAPI:
    def __init__(self) -> None:
        self.client_id = os.environ.get('NAVER_API_CLIENT_ID')
        self.client_secret = os.environ.get('NAVER_API_CLIENT_SECERT')