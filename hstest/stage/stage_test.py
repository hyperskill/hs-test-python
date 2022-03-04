import os
import unittest
from typing import Any, Dict, List, Optional, Tuple, Type

from hstest.common.file_utils import walk_user_files
from hstest.common.reflection_utils import is_tests, setup_cwd
from hstest.common.utils import failed, passed
from hstest.dynamic.input.dynamic_testing import DynamicTestElement, search_dynamic_tests
from hstest.dynamic.output.colored_output import RED_BOLD, RESET
from hstest.dynamic.output.output_handler import OutputHandler
from hstest.dynamic.system_handler import SystemHandler
from hstest.exception.failure_handler import get_exception_text, get_report
from hstest.exception.outcomes import OutcomeError, UnexpectedError, WrongAnswer
from hstest.outcomes.outcome import Outcome
from hstest.test_case.check_result import CheckResult
from hstest.test_case.test_case import TestCase
from hstest.testing.execution.main_module_executor import MainModuleExecutor
from hstest.testing.execution.process.go_executor import GoExecutor
from hstest.testing.execution.process.javascript_executor import JavascriptExecutor
from hstest.testing.execution.process.python_executor import PythonExecutor
from hstest.testing.execution.process.shell_executor import ShellExecutor
from hstest.testing.execution_options import force_process_testing
from hstest.testing.runner.async_dynamic_testing_runner import AsyncDynamicTestingRunner
from hstest.testing.runner.test_runner import TestRunner
from hstest.testing.test_run import TestRun


class DirMeta(type):
    def __dir__(self):
        if not issubclass(self, StageTest) or self == StageTest:
            return []
        init_dir = dir(super(DirMeta, self)) + list(self.__dict__.keys())
        filtered_dir = list(filter(lambda x: not str(x).startswith('test'), init_dir))
        filtered_dir.append('test_run_unittest')
        if not self.dynamic_methods() and 'generate' not in init_dir:
            return []
        return set(filtered_dir)


class StageTest(unittest.TestCase, metaclass=DirMeta):
    runner: TestRunner = None
    attach: Any = None

    source: str = None
    curr_test_run: Optional[TestRun] = None
    curr_test_global: int = 0

    def __init__(self, args, source_name: str = ''):
        super(StageTest, self).__init__(args)
        self.is_tests = False

        if self.source:
            self.source_name: str = self.source
        else:
            self.source_name: str = source_name

    def test_run_unittest(self):
        result, feedback = self.run_tests(is_unittest=True)
        if result != 0:
            self.fail(feedback)

    def after_all_tests(self):
        pass

    def _init_runner(self) -> TestRunner:
        for folder, dirs, files in walk_user_files(os.getcwd()):
            for f in files:
                if f.endswith('.go'):
                    return AsyncDynamicTestingRunner(GoExecutor)

                if f.endswith('.js'):
                    return AsyncDynamicTestingRunner(JavascriptExecutor)

                if f.endswith('.sh'):
                    return AsyncDynamicTestingRunner(ShellExecutor)

                if f.endswith('.py'):
                    if force_process_testing:
                        return AsyncDynamicTestingRunner(PythonExecutor)
                    else:
                        return AsyncDynamicTestingRunner(MainModuleExecutor)

        return AsyncDynamicTestingRunner(MainModuleExecutor)

    def _init_tests(self) -> List[TestRun]:
        if self.runner is None:
            self.runner = self._init_runner()

        test_runs: List[TestRun] = []
        test_cases: List[TestCase] = list(self.generate())
        test_cases += search_dynamic_tests(self)

        if len(test_cases) == 0:
            raise UnexpectedError("No tests found")

        curr_test: int = 0
        test_count = len(test_cases)
        for test_case in test_cases:
            test_case.source_name = self.source_name
            if test_case.check_func is None:
                test_case.check_func = self.check
            if test_case.attach is None:
                test_case.attach = self.attach
            curr_test += 1
            test_runs += [
                TestRun(curr_test, test_count, test_case, self.runner)
            ]

        return test_runs

    def __print_test_num(self, num: int):
        total_tests = '' if num == self.curr_test_global else f' ({self.curr_test_global})'
        OutputHandler.get_real_out().write(
            RED_BOLD + f'\nStart test {num}{total_tests}' + RESET + '\n'
        )

    def run_tests(self, *, debug=False, is_unittest: bool = False) -> Tuple[int, str]:
        curr_test: int = 0
        need_tear_down: bool = False
        try:
            if is_tests(self):
                self.is_tests = True
                setup_cwd(self)

            if self.is_tests or debug:
                import hstest.common.utils as hs
                hs.failed_msg_start = ''
                hs.failed_msg_continue = ''
                hs.success_msg = ''

            SystemHandler.set_up()
            test_runs = self._init_tests()

            for test_run in test_runs:
                curr_test += 1
                StageTest.curr_test_global += 1
                self.__print_test_num(curr_test)

                if test_run.is_first_test():
                    test_run.set_up()
                    need_tear_down = True

                StageTest.curr_test_run = test_run
                result: CheckResult = test_run.test()

                if not result.is_correct:
                    full_feedback = result.feedback + '\n\n' + test_run.test_case.feedback
                    raise WrongAnswer(full_feedback.strip())

                if test_run.is_last_test():
                    need_tear_down = False
                    test_run.tear_down()

            SystemHandler.tear_down()
            return passed(is_unittest)

        except BaseException as ex:
            if need_tear_down:
                try:
                    StageTest.curr_test_run.tear_down()
                except BaseException as new_ex:
                    if isinstance(new_ex, OutcomeError):
                        ex = new_ex

            build = 'hs-test-python'

            try:
                report = build + "\n\n" + get_report()
            except:
                report = build

            try:
                outcome: Outcome = Outcome.get_outcome(ex, curr_test)
                fail_text = str(outcome)
            except BaseException as new_ex:
                try:
                    outcome: Outcome = Outcome.get_outcome(new_ex, curr_test)
                    fail_text = str(outcome)
                except BaseException as new_ex2:
                    try:
                        traceback = ""

                        for e in new_ex2, new_ex, ex:
                            try:
                                text = get_exception_text(e)
                            except:
                                try:
                                    text = f'{type(e)}: {str(e)}'
                                except:
                                    text = 'Broken exception'

                            if len(text):
                                traceback += text + "\n\n"

                        fail_text = 'Unexpected error\n\n' + report + "\n\n" + traceback

                    except BaseException:
                        # no code execution here allowed so not to throw an exception
                        fail_text = 'Unexpected error\n\nCannot check the submission\n\n' + report

            try:
                SystemHandler.tear_down()
            except BaseException:
                pass

            return failed(fail_text, is_unittest)

        finally:
            StageTest.curr_test_run = None
            StageTest.runner = None
            StageTest.attach = None
            StageTest.source = None
            self.after_all_tests()

    _dynamic_methods: Dict[Type['StageTest'], List[DynamicTestElement]] = {}

    @classmethod
    def dynamic_methods(cls) -> List[DynamicTestElement]:
        if cls in StageTest._dynamic_methods:
            return StageTest._dynamic_methods[cls]
        empty = []
        StageTest._dynamic_methods[cls] = empty
        return empty

    def generate(self) -> List[TestCase]:
        return []

    def check(self, reply: str, attach: Any) -> CheckResult:
        raise UnexpectedError('Can\'t check result: override "check" method')
