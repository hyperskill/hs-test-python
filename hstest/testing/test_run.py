from typing import List, Optional

from hstest.check_result import CheckResult, correct
from hstest.common.file_utils import create_files, delete_files
from hstest.dynamic.output.output_handler import OutputHandler
from hstest.dynamic.system_handler import SystemHandler
from hstest.exception.outcomes import ExceptionWithFeedback, UnexpectedError
from hstest.exceptions import TestPassed
from hstest.test_case.test_case import TestCase
from hstest.testing.runner.test_runner import TestRunner
from hstest.testing.settings import Settings
from hstest.testing.tested_program import TestedProgram


class TestRun:
    def __init__(self, test_num: int, test_count: int,
                 test_case: TestCase, test_rummer: TestRunner):
        self._test_num: int = test_num
        self._test_count: int = test_count
        self._test_case: TestCase = test_case
        self._test_runner: TestRunner = test_rummer

        self._input_used: bool = False
        self._error_in_test: Optional[BaseException] = None
        self._tested_programs: List[TestedProgram] = []

    def is_first_test(self) -> bool:
        return self._test_num == 1

    def is_last_test(self) -> bool:
        return self._test_num == self._test_count

    @property
    def test_num(self) -> int:
        return self._test_num

    @property
    def test_count(self) -> int:
        return self._test_count

    @property
    def test_case(self) -> TestCase:
        return self._test_case

    @property
    def test_runner(self) -> TestRunner:
        return self._test_runner

    @property
    def input_used(self) -> bool:
        return self._input_used

    @property
    def tested_programs(self) -> List[TestedProgram]:
        return self._tested_programs

    @property
    def error_in_test(self) -> Optional[BaseException]:
        return self._error_in_test

    def set_error_in_test(self, err: Optional[BaseException]):
        if self._error_in_test is None or err is None:
            self._error_in_test = err

    def set_input_used(self):
        self._input_used = True

    def add_tested_program(self, tested_program: TestedProgram):
        self._tested_programs += [tested_program]

    def stop_tested_programs(self):
        for tested_program in self._tested_programs:
            tested_program.stop()

    def invalidate_handlers(self):
        for tested_program in self._tested_programs:
            SystemHandler.uninstall_handler(tested_program.executor)

    def set_up(self):
        self._test_runner.set_up(self._test_case)

    def tear_down(self):
        self._test_runner.tear_down(self._test_case)

    def test(self) -> CheckResult:
        create_files(self._test_case.files)
        # startThreads(testCase.getProcesses())

        if Settings.do_reset_output:
            OutputHandler.reset_output()

        result = None
        try:
            result = self._test_runner.test(self)
        except BaseException as ex:
            self.set_error_in_test(ex)

        # stopThreads(testCase.getProcesses(), pool)
        delete_files(self._test_case.files)

        if result is None:
            self._check_errors()

        if isinstance(self._error_in_test, TestPassed):
            result = correct()

        if result is None:
            raise UnexpectedError("Result is None after testing")

        return result

    def _check_errors(self):
        error_in_test = self._error_in_test
        test_case = self._test_case

        if error_in_test is None:
            return

        if isinstance(error_in_test, TestPassed):
            return

        if isinstance(error_in_test, ExceptionWithFeedback):
            user_exception = error_in_test.real_exception

            for exception, feedback in test_case.feedback_on_exception.items():
                ex_type = type(user_exception)

                exact_subclass = ex_type is not None and issubclass(ex_type, exception)
                if exact_subclass:
                    raise ExceptionWithFeedback(feedback, user_exception)

                if user_exception is None:
                    hint_in_feedback = exception.__name__ in error_in_test.error_text

                    if hint_in_feedback:
                        raise ExceptionWithFeedback(
                            feedback + '\n\n' + error_in_test.error_text, None
                        )

        raise error_in_test
