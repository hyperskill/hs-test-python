from hstest.common.utils import get_stacktrace, get_report
from hstest.dynamic.output.output_handler import OutputHandler
from hstest.exception.outcomes import ExceptionWithFeedback, ErrorWithFeedback, UnexpectedError
from hstest.exception.testing import TimeLimitException
from hstest.exceptions import WrongAnswer
from hstest.testing.test_run import TestRun


class Outcome:
    def __init__(self):
        self.test_number: int = 0
        self.error_text: str = ''
        self.stack_trace: str = ''

    def get_type(self) -> str:
        raise NotImplementedError()

    def __str__(self):
        if self.test_number == 0:
            when_error_happened = ' during testing'
        else:
            when_error_happened = f' in test #{self.test_number}'

        result = self.get_type() + when_error_happened

        if self.error_text:
            result += '\n\n' + self.error_text.strip()

        if self.stack_trace:
            result += '\n\n' + self.stack_trace.strip()

        full_log = OutputHandler.get_dynamic_output()

        if len(full_log.strip()) > 0:
            result += ('\n\nPlease find below the output '
                       'of your program during this failed test.\n')
            if TestRun.curr_test_run.input_used:
                result += ("Note that the '>' character indicates "
                           "the beginning of the input line.\n")
            result += '\n---\n\n'
            result += full_log

        return result.strip()

    @staticmethod
    def get_outcome(ex: BaseException, stage, test_num: int):
        if isinstance(ex, WrongAnswer):
            return WrongAnswerOutcome(test_num, ex.feedback)

        elif isinstance(ex, ExceptionWithFeedback):
            return ExceptionOutcome(test_num, ex.real_exception, ex.feedback, stage)

        elif isinstance(ex, ErrorWithFeedback) or \
                isinstance(ex, TimeLimitException) or \
                isinstance(ex, PermissionError):
            return ErrorOutcome(test_num, ex)

        if isinstance(ex, UnexpectedError) and ex.exception is not None:
            ex = ex.exception
        return UnexpectedErrorOutcome(test_num, ex, stage)


class WrongAnswerOutcome(Outcome):
    def __init__(self, test_num: int, feedback: str):
        super().__init__()
        self.test_number = test_num
        self.error_text = feedback

    def get_type(self) -> str:
        return 'Wrong answer'


class ExceptionOutcome(Outcome):
    def __init__(self, test_num: int, cause: BaseException, feedback: str, stage):
        super().__init__()
        self.test_number = test_num
        self.error_text = feedback
        self.stack_trace = get_stacktrace(stage.path_to_test, cause, hide_internals=True)

        if self.stack_trace.strip().endswith('EOFError: EOF when reading a line'):
            self.error_text += '\n\nProbably your program run out of input (tried to read more than expected)'

    def get_type(self) -> str:
        return 'Exception'


class ErrorOutcome(Outcome):
    def __init__(self, test_num: int, cause: BaseException):
        super().__init__()
        self.test_number = test_num

        if isinstance(cause, TimeLimitException):
            time_limit: int = cause.time_limit_ms
            time_unit: str = 'milliseconds'
            if time_limit > 1999:
                time_limit //= 1000
                time_unit = 'seconds'
            self.error_text = (
                'In this test, the program is running for a long time, ' +
                f'more than {time_limit} {time_unit}. Most likely, ' +
                'the program has gone into an infinite loop.'
            )

        elif isinstance(cause, PermissionError):
            self.error_text = (
                "The file you opened " +
                "can't be deleted after the end of the test. " +
                "Probably you didn't close it."
            )

        elif isinstance(cause, ErrorWithFeedback):
            self.error_text = cause.error_text

    def get_type(self) -> str:
        return 'Error'


class UnexpectedErrorOutcome(Outcome):
    def __init__(self, test_num: int, cause: BaseException, stage):
        super().__init__()
        self.test_number = test_num
        self.error_text = 'We have recorded this bug ' \
                          'and will fix it soon.\n\n' + get_report()
        self.stack_trace = get_stacktrace(stage.path_to_test, cause, hide_internals=False)

    def get_type(self) -> str:
        return 'Unexpected error'
