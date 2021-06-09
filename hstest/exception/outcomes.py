from typing import Optional


class OutcomeError(BaseException):
    pass


class SyntaxException(OutcomeError):
    def __init__(self, exception: SyntaxError, file: str):
        self.file: str = file
        self.exception: SyntaxError = exception


class ExceptionWithFeedback(OutcomeError):
    def __init__(self, error_text: str, real_exception: Optional[BaseException]):
        self.error_text: str = error_text
        self.real_exception: BaseException = real_exception


class ErrorWithFeedback(OutcomeError):
    def __init__(self, error_text: str):
        self.error_text = error_text


class UnexpectedError(OutcomeError):
    def __init__(self, error_text: str, ex: Optional[BaseException] = None):
        self.error_text = error_text
        self.exception = ex


class CompilationError(OutcomeError):
    def __init__(self, error_text: str):
        self.error_text = error_text


class TestPassed(OutcomeError):
    pass


class WrongAnswer(OutcomeError):
    def __init__(self, feedback: str):
        self.feedback = feedback
