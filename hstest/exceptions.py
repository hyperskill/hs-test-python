from typing import Optional


class SyntaxException(BaseException):
    def __init__(self, exception: BaseException, file: str):
        self.file: str = file
        self.exception: BaseException = exception


class ExitException(BaseException):
    @staticmethod
    def throw():
        raise ExitException()


class ExceptionWithFeedback(BaseException):
    def __init__(self, feedback: str, real_exception: BaseException):
        self.feedback: str = feedback
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
    def __init__(self, feedback: str):
        self.feedback = feedback
