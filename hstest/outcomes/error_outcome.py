from hstest.exception.outcomes import ErrorWithFeedback
from hstest.exception.testing import FileDeletionError, InfiniteLoopException, TimeLimitException
from hstest.outcomes.outcome import Outcome


class ErrorOutcome(Outcome):
    def __init__(self, test_num: int, cause: BaseException):
        super().__init__()
        self.test_number = test_num

        if isinstance(cause, FileDeletionError):
            self._init_permission_error(cause)

        elif isinstance(cause, TimeLimitException):
            self._init_time_limit_exception(cause)

        elif isinstance(cause, ErrorWithFeedback):
            self.error_text = cause.error_text

        elif isinstance(cause, InfiniteLoopException):
            self.error_text = "Infinite loop detected.\n" + cause.message

    def _init_permission_error(self, _: FileDeletionError):
        self.error_text = (
            "The file you opened " +
            "can't be deleted after the end of the test. " +
            "Probably you didn't close it."
        )

    def _init_time_limit_exception(self, ex: TimeLimitException):
        time_limit: int = ex.time_limit_ms
        time_unit: str = 'milliseconds'
        if time_limit > 1999:
            time_limit //= 1000
            time_unit = 'seconds'
        self.error_text = (
            'In this test, the program is running for a long time, ' +
            f'more than {time_limit} {time_unit}. Most likely, ' +
            'the program has gone into an infinite loop.'
        )

    def get_type(self) -> str:
        return 'Error'
