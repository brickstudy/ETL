from enum import Enum


class Naver(Enum):
    AuthError = {
        "code": 401,
        "message": "Naver 개발자 계정 정보를 확인하세요."
    }

    UnknownError = {
        "code": 401,
        "message": "확인되지 않은 오류입니다."
    }
