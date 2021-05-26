from hstest.common.reflection_utils import get_stacktrace, str_to_stacktrace
from hstest.exception.outcomes import ExceptionWithFeedback
from hstest.outcomes.outcome import Outcome


class ExceptionOutcome(Outcome):
    def __init__(self, test_num: int, ex: ExceptionWithFeedback):
        super().__init__()
        cause = ex.real_exception
        feedback = ex.error_text

        self.test_number = test_num

        if cause is not None:
            self.stack_trace = get_stacktrace(cause, hide_internals=True)
            self.error_text = feedback

        else:
            self.stack_trace = str_to_stacktrace(feedback)
            self.error_text = ''

        eof = 'EOFError: EOF when reading a line'
        eof_feedback = 'Probably your program run out of input (tried to read more than expected)'

        if self.stack_trace.strip().endswith(eof):
            self.error_text += '\n\n' + eof_feedback

    def get_type(self) -> str:
        return 'Exception'
