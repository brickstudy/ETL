from enum import Enum


class Naver(Enum):
    AuthError = {
        "code": 401,
        "message": "Naver 개발자 계정 정보를 확인하세요."
    }

    HTTPUnknownError = {
        "code": 000,
        "message": "Auth, Limit 이외 HTTP 관련 오류입니다."
    }

    LimitExceedError = {
        "code": 429,
        "message": "하루 요청 허용량을 초과했습니다."
    }

    UrlError = {
        "code": 000,
        "message": "URL 관련 오류입니다."
    }

    UnknownError = {
        "code": 000,
        "message": "확인되지 않은 오류입니다."
    }


class NewsApi(Enum):
    AuthError = {
        "code": 401,
        "message": "News api 토큰 정보를 확인하세요."
    }

    UnknownError = {
        "code": 000,
        "message": "확인되지 않은 오류입니다."
    }
