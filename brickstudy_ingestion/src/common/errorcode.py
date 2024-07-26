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

    LimitExceedError = {
        "code": 429,
        "message": "하루 요청 허용량을 초과했습니다."
    }
