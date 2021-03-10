from typing import Any, Dict, List, Optional, Tuple, Type

from hstest.common.reflection_utils import is_tests, setup_cwd
from hstest.common.utils import failed, passed
from hstest.dynamic.input.dynamic_testing import DynamicTestElement, search_dynamic_tests
from hstest.dynamic.output.colored_output import RED_BOLD, RESET
from hstest.dynamic.output.output_handler import OutputHandler
from hstest.dynamic.system_handler import SystemHandler
from hstest.exception.outcomes import OutcomeError, UnexpectedError, WrongAnswer
from hstest.outcomes.outcome import Outcome
from hstest.test_case.check_result import CheckResult
from hstest.test_case.test_case import TestCase
from hstest.testing.runner.async_main_file_runner import AsyncMainFileRunner
from hstest.testing.runner.test_runner import TestRunner
from hstest.testing.test_run import TestRun


class StageTest:
    runner: TestRunner = AsyncMainFileRunner()
    attach: Any = None

    source: str = None
    curr_test_run: Optional[TestRun] = None
    _curr_test_global: int = 0

    def __init__(self, source_name: str = ''):
        if self.source:
            self.source_name: str = self.source
        else:
            self.source_name: str = source_name
        # super().__init__(method)
        # self.module =

    # def test_program(self):
    #    result, feedback = self.run_tests()
    #     if result != 0:
    #         self.fail(feedback)

    def after_all_tests(self):
        pass

    def _init_tests(self) -> List[TestRun]:
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
        total_tests = '' if num == self._curr_test_global else f' ({self._curr_test_global})'
        OutputHandler.get_real_out().write(
            RED_BOLD + f'\nStart test {num}{total_tests}' + RESET + '\n'
        )

    def run_tests(self, *, debug=False) -> Tuple[int, str]:
        if is_tests(self) or debug:
            setup_cwd(self)

            import hstest.common.utils as hs
            hs.failed_msg_start = ''
            hs.failed_msg_continue = ''
            hs.success_msg = ''

        curr_test: int = 0
        need_tear_down: bool = False
        try:
            SystemHandler.set_up()
            test_runs = self._init_tests()

            for test_run in test_runs:
                curr_test += 1
                StageTest._curr_test_global += 1
                self.__print_test_num(curr_test)

                if test_run.is_first_test():
                    test_run.set_up()
                    need_tear_down = True

                StageTest.curr_test_run = test_run
                result: CheckResult = test_run.test()

                if not result.is_correct:
                    raise WrongAnswer(result.feedback)

                if test_run.is_last_test():
                    need_tear_down = False
                    test_run.tear_down()

            SystemHandler.tear_down()
            return passed()

        except BaseException as ex:
            if need_tear_down:
                try:
                    StageTest.curr_test_run.tear_down()
                except BaseException as new_ex:
                    if isinstance(new_ex, OutcomeError):
                        ex = new_ex
            outcome: Outcome = Outcome.get_outcome(ex, curr_test)
            fail_text = str(outcome)
            SystemHandler.tear_down()
            return failed(fail_text)

        finally:
            StageTest.curr_test_run = None
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
