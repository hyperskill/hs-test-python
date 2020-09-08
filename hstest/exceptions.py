from typing import Optional


class OutcomeError(BaseException):
    pass


class SyntaxException(OutcomeError):
    def __init__(self, exception: SyntaxError, file: str):
        self.file: str = file
        self.exception: SyntaxError = exception


class ExceptionWithFeedback(OutcomeError):
    def __init__(self, feedback: str, real_exception: BaseException):
        self.feedback: str = feedback
        self.real_exception: BaseException = real_exception


class ErrorWithFeedback(OutcomeError):
    def __init__(self, error_text: str):
        self.error_text = error_text


class UnexpectedError(OutcomeError):
    def __init__(self, error_text: str, ex: Optional[BaseException] = None):
        self.error_text = error_text
        self.exception = ex


class TestPassed(OutcomeError):
    pass


# simple rename, but have to be sure old tests work as expected
TestPassedException = TestPassed


class WrongAnswer(OutcomeError):
    def __init__(self, feedback: str):
        self.feedback = feedback


# simple rename, but have to be sure old tests work as expected
WrongAnswerException = WrongAnswer


class TimeLimitException(BaseException):
    def __init__(self, time_limit_ms: int):
        self.time_limit_ms: int = time_limit_ms


class ExitException(BaseException):
    @staticmethod
    def throw():
        raise ExitException()
