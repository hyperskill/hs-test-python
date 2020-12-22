from hstest.common.reflection_utils import get_stacktrace
from hstest.exception.outcomes import ExceptionWithFeedback
from hstest.outcomes.outcome import Outcome


class ExceptionOutcome(Outcome):
    def __init__(self, test_num: int, ex: ExceptionWithFeedback):
        super().__init__()
        cause = ex.real_exception
        feedback = ex.error_text

        self.test_number = test_num
        self.stack_trace = get_stacktrace(cause, hide_internals=True)

        self.error_text = feedback

        if self.stack_trace.strip().endswith('EOFError: EOF when reading a line'):
            self.error_text += '\n\nProbably your program run out of input (tried to read more than expected)'

    def get_type(self) -> str:
        return 'Exception'
