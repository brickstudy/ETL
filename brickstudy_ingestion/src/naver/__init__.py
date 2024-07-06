import os
from dotenv import load_dotenv


# .env 파일 로드
load_dotenv()


client_id = os.getenv('NAVER_API_CLIENT_ID')
client_secret = os.getenv('NAVER_API_CLIENT_SECERT')
