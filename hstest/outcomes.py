import os
from hstest.exceptions import WrongAnswerException
from hstest.exceptions import ExceptionWithFeedback
from hstest.exceptions import TimeLimitException
from hstest.exceptions import FatalErrorException
from hstest.utils import get_stacktrace, get_report
from hstest.dynamic.handle_stdout import StdoutHandler
from hstest.test_run import TestRun


class Outcome:
    def __init__(self):
        self.test_number: int = 0
        self.error_text: str = ''
        self.stack_trace: str = ''

    def get_type(self) -> str:
        raise NotImplementedError()

    def get_type_suffix(self) -> str:
        return ''

    def __str__(self):
        if self.test_number == 0:
            when_error_happened = ' during testing'
        else:
            when_error_happened = f' in test #{self.test_number}'

        result = self.get_type() + when_error_happened + self.get_type_suffix()

        if self.error_text:
            result += '\n\n' + self.error_text.strip()

        if self.stack_trace:
            result += '\n\n' + self.stack_trace.strip()

        full_log = StdoutHandler.get_dynamic_output()

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
        if isinstance(ex, WrongAnswerException):
            return WrongAnswerOutcome(test_num, ex.feedback)
        elif isinstance(ex, ExceptionWithFeedback):
            return ExceptionOutcome(test_num, ex.real_exception, ex.feedback, stage)
        elif isinstance(ex, TimeLimitException):
            return ErrorOutcome(test_num, ex)

        if isinstance(ex, FatalErrorException) and ex.exception is not None:
            ex = ex.exception
        return FatalErrorOutcome(test_num, ex, stage)


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
        self.stack_trace = get_stacktrace(stage.file_to_test, cause, hide_internals=True)

        if self.stack_trace.strip().endswith('EOFError: EOF when reading a line'):
            self.error_text += '\n\nProbably your program run out of input'

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

    def get_type(self) -> str:
        return 'Error'


class FatalErrorOutcome(Outcome):
    def __init__(self, test_num: int, cause: BaseException, stage):
        super().__init__()
        self.test_number = test_num
        self.error_text = get_report()
        self.stack_trace = get_stacktrace(stage.file_to_test, cause, hide_internals=False)

    def get_type(self) -> str:
        return 'Fatal error'

    def get_type_suffix(self) -> str:
        return ', please send the report to support@hyperskill.org'


class SyntaxErrorOutcome(Outcome):
    def __init__(self, cause: SyntaxError, stage):
        super().__init__()

        file = cause.filename
        file = file.replace(os.sep, '.')
        file = file[file.index(stage.module_to_test):-3]
        file = file.replace('.', os.sep) + '.py'

        output = f'File "{file}", line {cause.lineno}\n' \
                 + cause.text.strip()[: cause.offset - 1] + '\n' \
                 'SyntaxError: invalid syntax'

        self.error_text = output

    def get_type(self) -> str:
        return 'Syntax error'

    def __str__(self):
        return self.error_text
