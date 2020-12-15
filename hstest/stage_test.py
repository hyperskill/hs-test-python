from typing import List, Any, Tuple, Optional, Type

from hstest.check_result import CheckResult
from hstest.common.utils import failed, passed
from hstest.dynamic.input.dynamic_testing import search_dynamic_tests
from hstest.dynamic.output.colored_output import RED_BOLD, RESET
from hstest.dynamic.output.output_handler import OutputHandler
from hstest.dynamic.system_handler import SystemHandler
from hstest.exception.outcomes import UnexpectedError
from hstest.exceptions import *
from hstest.outcomes import Outcome
from hstest.test_case import TestCase
from hstest.testing.runner.async_main_file_runner import AsyncMainFileRunner
from hstest.testing.runner.test_runner import TestRunner
from hstest.testing.test_run import TestRun


class StageTest:
    _dynamic_methods = {}
    _dynamic_variables = {}

    runner: Type[TestRunner] = AsyncMainFileRunner
    curr_test_run: Optional[TestRun] = None
    curr_test_global: int = 0

    # def run_tests(self):
    #     for i in self._dynamic_methods.get(type(self), []):
    #         i(self)

    def __init__(self, source_name: str = ''):
        self.source_name: str = source_name
        # super().__init__(method)
        # self.module =

    # def reset(self):
    #     top_module = self.module_to_test[:self.module_to_test.rindex('.')]
    #     for name, module in list(sys.modules.items()):
    #         if name.startswith(top_module):
    #             importlib.reload(module)

    # def test_program(self):
    #    result, feedback = self.run_tests()
    #     if result != 0:
    #         self.fail(feedback)

    def after_all_tests(self):
        pass

    def _init_tests(self) -> List[TestRun]:
        test_runs: List[TestRun] = []
        test_cases: List[TestCase] = list(self.generate())
        test_cases += search_dynamic_tests()

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
        if self.source_name.startswith('tests.') or debug:
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

            return passed()

        except BaseException as ex:
            outcome: Outcome = Outcome.get_outcome(ex, curr_test)
            fail_text = str(outcome)
            return failed(fail_text)

        finally:
            StageTest.curr_test_run = None
            self.after_all_tests()
            SystemHandler.tear_down()

    def generate(self) -> List[TestCase]:
        return []

    def check(self, reply: str, attach: Any) -> CheckResult:
        raise UnexpectedError('Can\'t check result: override "check" method')
