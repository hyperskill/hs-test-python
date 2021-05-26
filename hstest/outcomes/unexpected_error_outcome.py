from hstest.common.reflection_utils import get_stacktrace
from hstest.dynamic.output.output_handler import OutputHandler
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

        program_stderr: str = OutputHandler.get_err()
        if program_stderr:
            self.stack_trace = self.stack_trace.strip() + '\n\n' + program_stderr

    def get_type(self) -> str:
        return 'Unexpected error'
