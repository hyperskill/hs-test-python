from __future__ import annotations

import concurrent.futures
import typing

from hstest.common.process_utils import DaemonThreadPoolExecutor
from hstest.dynamic.output.output_handler import OutputHandler
from hstest.exception.testing import (
    TestedProgramFinishedEarly,
    TestedProgramThrewException,
    TimeLimitException,
)
from hstest.exceptions import TestPassed, WrongAnswer
from hstest.test_case.check_result import CheckResult, correct, wrong
from hstest.testing.execution.main_module_executor import MainModuleExecutor
from hstest.testing.execution_options import debug_mode
from hstest.testing.runner.test_runner import TestRunner

if typing.TYPE_CHECKING:
    from concurrent.futures import Future

    from hstest import TestCase
    from hstest.testing.execution.program_executor import ProgramExecutor
    from hstest.testing.test_run import TestRun


class AsyncDynamicTestingRunner(TestRunner):
    def __init__(self, executor: type[ProgramExecutor] = MainModuleExecutor) -> None:
        self.executor: type[ProgramExecutor] = executor

    def _run_dynamic_test(self, test_run: TestRun) -> CheckResult:
        test_case = test_run.test_case
        try:
            result = test_case.dynamic_testing()
        except WrongAnswer as wa:
            result = wrong(wa.feedback)
        except TestPassed:
            result = correct()
        except (TestedProgramThrewException, TestedProgramFinishedEarly):
            result = None

        if result is None or result.is_correct:
            test_run.stop_tested_programs()

        return result

    def _run_file(self, test_run: TestRun) -> CheckResult | None:
        test_case = test_run.test_case
        time_limit = test_case.time_limit

        executor = DaemonThreadPoolExecutor(name=f"AsyncMainFileRunner test #{test_run.test_num}")
        try:
            future: Future = executor.submit(lambda: self._run_dynamic_test(test_run))
            if time_limit <= 0 or debug_mode:
                return future.result()
            return future.result(timeout=time_limit / 1000)
        except concurrent.futures.TimeoutError:
            test_run.set_error_in_test(TimeLimitException(time_limit))
        except (
            AssertionError,
            WrongAnswer,
            TestPassed,
            TestedProgramThrewException,
            TestedProgramFinishedEarly,
        ) as ex:
            test_run.set_error_in_test(ex)
        # Let unexpected exceptions propagate.
            test_run.set_error_in_test(ex)
        finally:
            test_run.invalidate_handlers()
            executor.shutdown(wait=False)

        return None

    def test(self, test_run: TestRun) -> CheckResult | None:
        test_case = test_run.test_case

        result: CheckResult = self._run_file(test_run)

        if result is None:
            error = test_run.error_in_test

            if error is None:
                try:
                    return test_case.check_func(OutputHandler.get_output(), test_case.attach)
                except (
                    AssertionError,
                    WrongAnswer,
                    TestPassed,
                    TestedProgramThrewException,
                    TestedProgramFinishedEarly,
                ) as ex:
                    error = ex
                    test_run.set_error_in_test(error)
                # Do not catch all Exception; let unexpected exceptions propagate.
                    error = ex
                    test_run.set_error_in_test(error)

            return CheckResult.from_error(error)

        return result

    def tear_down(self, test_case: TestCase) -> None:
        from hstest import StageTest

        for program in StageTest.curr_test_run.tested_programs:
            program.executor.tear_down()
