from typing import Optional


class SyntaxException(BaseException):
    def __init__(self, exception: SyntaxError, file: str):
        self.file: str = file
        self.exception: SyntaxError = exception


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


class TestPassed(BaseException):
    pass


# simple rename, but have to be sure old tests work as expected
TestPassedException = TestPassed


class TimeLimitException(BaseException):
    def __init__(self, time_limit_ms: int):
        self.time_limit_ms: int = time_limit_ms


class WrongAnswer(BaseException):
    def __init__(self, feedback: str):
        self.feedback = feedback


# simple rename, but have to be sure old tests work as expected
WrongAnswerException = WrongAnswer
