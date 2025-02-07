from __future__ import annotations


class OutcomeError(BaseException):
    pass


class SyntaxException(OutcomeError):
    def __init__(self, exception: SyntaxError, file: str) -> None:
        self.file: str = file
        self.exception: SyntaxError = exception


class ExceptionWithFeedback(OutcomeError):
    def __init__(self, error_text: str, real_exception: BaseException | None) -> None:
        self.error_text: str = error_text
        self.real_exception: BaseException = real_exception


class ErrorWithFeedback(OutcomeError):
    def __init__(self, error_text: str) -> None:
        self.error_text = error_text


class OutOfInputError(ErrorWithFeedback):
    def __init__(self) -> None:
        super().__init__("Program ran out of input. You tried to read more than expected.")


class UnexpectedError(OutcomeError):
    def __init__(self, error_text: str, ex: BaseException | None = None) -> None:
        self.error_text = error_text
        self.exception = ex


class CompilationError(OutcomeError):
    def __init__(self, error_text: str) -> None:
        self.error_text = error_text


class TestPassed(OutcomeError):
    pass


class WrongAnswer(OutcomeError):
    def __init__(self, feedback: str) -> None:
        self.feedback = feedback
