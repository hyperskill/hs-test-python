from __future__ import annotations


class TimeLimitException(BaseException):
    def __init__(self, time_limit_ms: int) -> None:
        self.time_limit_ms: int = time_limit_ms


class TestedProgramThrewException(BaseException):
    pass


class TestedProgramFinishedEarly(BaseException):
    pass


class InfiniteLoopException(BaseException):
    def __init__(self, message: str) -> None:
        self.message = message


class FileDeletionError(BaseException):
    pass
