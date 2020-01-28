from typing import Optional


class BadSolutionException(BaseException):
    def __init__(self, user_exception: BaseException):
        self.user_exception = user_exception


class SyntaxException(BaseException):
    def __init__(self, exception: BaseException, file: str):
        self.file: str = file
        self.exception: BaseException = exception


class ExitException(BaseException):
    @staticmethod
    def throw():
        raise ExitException()


class ExceptionWithFeedback(BaseException):
    def __init__(self, error_text: str, real_exception: BaseException):
        self.error_text: str = error_text
        self.real_exception: BaseException = real_exception


class FatalErrorException(BaseException):
    def __init__(self, error_text: str, ex: Optional[BaseException] = None):
        self.error_text = error_text
        self.exception = ex


class TestPassedException(BaseException):
    pass


class TimeLimitException(BaseException):
    def __init__(self, time_limit_ms: int):
        self.time_limit_ms: int = time_limit_ms


class WrongAnswerException(BaseException):
    def __init__(self, error_text: str):
        self.error_text = error_text
