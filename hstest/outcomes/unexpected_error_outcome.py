from hstest.common.reflection_utils import get_stacktrace
from hstest.exception.failure_handler import get_report
from hstest.exception.outcomes import UnexpectedError
from hstest.outcomes.outcome import Outcome


class UnexpectedErrorOutcome(Outcome):
    def __init__(self, test_num: int, cause: BaseException):
        super().__init__()
        self.test_number = test_num
        self.error_text = 'We have recorded this bug ' \
                          'and will fix it soon.\n\n' + get_report()
        self.stack_trace = get_stacktrace(cause, hide_internals=False)
        if isinstance(cause, UnexpectedError) and cause.exception is not None:
            self.stack_trace += '\n' + get_stacktrace(cause.exception, hide_internals=False)

    def get_type(self) -> str:
        return 'Unexpected error'
