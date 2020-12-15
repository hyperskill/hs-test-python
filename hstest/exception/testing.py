
class TimeLimitException(BaseException):
    def __init__(self, time_limit_ms: int):
        self.time_limit_ms: int = time_limit_ms


class TestedProgramThrewException(BaseException):
    pass


class TestedProgramFinishedEarly(BaseException):
    pass


class InfiniteLoopException(BaseException):
    def __init__(self, message: str):
        self.message = message
