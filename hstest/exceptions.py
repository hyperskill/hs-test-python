class BadSolutionException(Exception):
    def __init__(self, message):
        self.message = message


class SyntaxException(BadSolutionException):
    def __init__(self, message):
        super().__init__(message)


class ExitException(BadSolutionException):
    def __init__(self, message):
        super().__init__(message)


class ExceptionWithFeedback(Exception):
    def __init__(self, error_text: str, real_exception: BaseException):
        self.error_text: str = error_text
        self.real_exception: BaseException = real_exception


class FatalErrorException(Exception):
    def __init__(self, error_text: str):
        self.error_text = error_text


class TestPassedException(Exception):
    pass


class TimeLimitException(Exception):
    def __init__(self, time_limit_ms: int):
        self.time_limit_ms: int = time_limit_ms


class WrongAnswerException(Exception):
    def __init__(self, error_text: str):
        self.error_text = error_text
