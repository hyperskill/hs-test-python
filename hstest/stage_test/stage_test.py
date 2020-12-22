from typing import Any, Dict, List, Optional, Tuple, Type

from hstest.common.reflection_utils import is_tests, setup_cwd
from hstest.common.utils import failed, passed
from hstest.dynamic.input.dynamic_testing import DynamicTestElement, search_dynamic_tests
from hstest.dynamic.output.colored_output import RED_BOLD, RESET
from hstest.dynamic.output.output_handler import OutputHandler
from hstest.dynamic.system_handler import SystemHandler
from hstest.exception.outcomes import UnexpectedError, WrongAnswer
from hstest.outcomes.outcome import Outcome
from hstest.test_case.check_result import CheckResult
from hstest.test_case.test_case import TestCase
from hstest.testing.runner.async_main_file_runner import AsyncMainFileRunner
from hstest.testing.runner.test_runner import TestRunner
from hstest.testing.test_run import TestRun


class StageTest:
    _dynamic_methods: Dict[Type['StageTest'], List[DynamicTestElement]] = {}

    runner: Type[TestRunner] = AsyncMainFileRunner
    curr_test_run: Optional[TestRun] = None
    curr_test_global: int = 0

    def __init__(self, source_name: str = ''):
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
            curr_test += 1
            test_runs += [
                TestRun(curr_test, test_count, test_case, self.runner())
            ]

        return test_runs

    def run_tests(self, *, debug=False) -> Tuple[int, str]:
        if is_tests(self) or debug:
            setup_cwd(self)

            import hstest.common.utils as hs
            hs.failed_msg_start = ''
            hs.failed_msg_continue = ''
            hs.success_msg = ''

        curr_test: int = 0
        try:
            SystemHandler.set_up()
            test_runs = self._init_tests()

            for test_run in test_runs:
                curr_test += 1
                StageTest.curr_test_global += 1
                total_tests = '' if curr_test == StageTest.curr_test_global else f' ({StageTest.curr_test_global})'
                OutputHandler.get_real_out().write(
                    RED_BOLD + f'\nStart test {curr_test}{total_tests}' + RESET + '\n'
                )

                StageTest.curr_test_run = test_run
                result: CheckResult = test_run.test()

                if not result.is_correct:
                    raise WrongAnswer(result.feedback)

            SystemHandler.tear_down()
            return passed()

        except BaseException as ex:
            outcome: Outcome = Outcome.get_outcome(ex, curr_test)
            fail_text = str(outcome)
            SystemHandler.tear_down()
            return failed(fail_text)

        finally:
            StageTest.curr_test_run = None
            self.after_all_tests()

    def generate(self) -> List[TestCase]:
        return []

    def check(self, reply: str, attach: Any) -> CheckResult:
        raise UnexpectedError('Can\'t check result: override "check" method')
