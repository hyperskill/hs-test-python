from hstest.common.utils import get_stacktrace, get_report
from hstest.dynamic.output.output_handler import OutputHandler
from hstest.exception.outcomes import ExceptionWithFeedback, ErrorWithFeedback, UnexpectedError
from hstest.exception.testing import TimeLimitException, InfiniteLoopException
from hstest.exceptions import WrongAnswer
from hstest.testing.test_run import TestRun


class Outcome:
    def __init__(self, test_number: int = 0, error_text: str = '', stack_trace: str = ''):
        self.test_number: int = test_number
        self.error_text: str = error_text
        self.stack_trace: str = stack_trace

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
        worth_showing_log = len(full_log.strip()) != 0 and full_log.strip() not in result

        arguments = ''

        from hstest.stage_test import StageTest
        test_run = StageTest.curr_test_run

        if test_run is not None:
            tested_programs = test_run.tested_programs
            programs_with_args = [p for p in tested_programs if len(p.run_args)]

            for pr in programs_with_args:
                arguments += 'Arguments'
                if len(tested_programs) > 1:
                    arguments += f' for {pr}'
                pr_args = [f'"{arg}"' if ' ' in arg else arg for arg in pr.run_args]
                arguments += f': {" ".join(pr_args)}\n'

        if worth_showing_log or len(arguments):
            result += '\n\n'
            if worth_showing_log:
                result += "Please find below the output of your program during this failed test.\n"
                if test_run.input_used:
                    result += "Note that the '>' character indicates the beginning of the input line.\n"
                result += "\n---\n\n"

            if len(arguments):
                result += arguments + '\n\n'

            if worth_showing_log:
                result += full_log

        return result.strip()

    @staticmethod
    def get_outcome(ex: BaseException, curr_test: int):
        if isinstance(ex, WrongAnswer):
            return WrongAnswerOutcome(curr_test, ex)

        elif isinstance(ex, ExceptionWithFeedback):
            return ExceptionOutcome(curr_test, ex)

        elif isinstance(ex, ErrorWithFeedback) or \
                isinstance(ex, PermissionError) or \
                isinstance(ex, TimeLimitException) or \
                isinstance(ex, InfiniteLoopException):
            return ErrorOutcome(curr_test, ex)

        # if isinstance(ex, UnexpectedError) and ex.exception is not None:
        #     ex = ex.exception
        return UnexpectedErrorOutcome(curr_test, ex)


class WrongAnswerOutcome(Outcome):
    def __init__(self, test_num: int, ex: WrongAnswer):
        super().__init__(test_num, ex.feedback, '')

    def get_type(self) -> str:
        return 'Wrong answer'


class ExceptionOutcome(Outcome):
    def __init__(self, test_num: int, ex: ExceptionWithFeedback):
        super().__init__()
        cause = ex.real_exception
        feedback = ex.error_text

        self.test_number = test_num
        self.stack_trace = get_stacktrace('', cause, hide_internals=True)

        self.error_text = feedback

        if self.stack_trace.strip().endswith('EOFError: EOF when reading a line'):
            self.error_text += '\n\nProbably your program run out of input (tried to read more than expected)'

    def get_type(self) -> str:
        return 'Exception'


class ErrorOutcome(Outcome):
    def __init__(self, test_num: int, cause: BaseException):
        super().__init__()
        self.test_number = test_num

        if isinstance(cause, PermissionError):
            self._init_permission_error(cause)

        elif isinstance(cause, TimeLimitException):
            self._init_time_limit_exception(cause)

        elif isinstance(cause, ErrorWithFeedback):
            self.error_text = cause.error_text

        elif isinstance(cause, InfiniteLoopException):
            self.error_text = "Infinite loop detected.\n" + cause.message

    def _init_permission_error(self, ex: PermissionError):
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


class UnexpectedErrorOutcome(Outcome):
    def __init__(self, test_num: int, cause: BaseException):
        super().__init__()
        self.test_number = test_num
        self.error_text = 'We have recorded this bug ' \
                          'and will fix it soon.\n\n' + get_report()
        self.stack_trace = get_stacktrace('', cause, hide_internals=False)
        if isinstance(cause, UnexpectedError) and cause.exception is not None:
            self.stack_trace += '\n' + get_stacktrace('', cause.exception, hide_internals=False)

    def get_type(self) -> str:
        return 'Unexpected error'
