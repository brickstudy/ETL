class BaseException(Exception):
    def __init__(self, code: int, message: str, log: any) -> None:
        self.code = code
        self.message = message
        self.log = log


class ExtractError(BaseException):
    def __init__(self, code: int, message: str, log: any) -> None:
        super().__init__(code, message, log)


class TransformError(BaseException):
    def __init__(self, code: int, message: str, log: any) -> None:
        super().__init__(code, message, log)


class LoadError(BaseException):
    def __init__(self, code: int, message: str, log: any) -> None:
        super().__init__(code, message, log)
