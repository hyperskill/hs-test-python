from concurrent.futures import Future, TimeoutError
from typing import Optional

from hstest.check_result import CheckResult, correct, wrong
from hstest.common.process_utils import DaemonThreadPoolExecutor
from hstest.dynamic.output.output_handler import OutputHandler
from hstest.exception.testing import TestedProgramFinishedEarly, TestedProgramThrewException, TimeLimitException
from hstest.exceptions import TestPassed, WrongAnswer
from hstest.testing.execution_options import debug_mode
from hstest.testing.runner.test_runner import TestRunner
from hstest.testing.test_run import TestRun


class AsyncMainFileRunner(TestRunner):
    def _run_dynamic_test(self, test_run: TestRun) -> CheckResult:
        test_case = test_run.test_case
        try:
            result = test_case.dynamic_testing()
        except WrongAnswer as wa:
            result = wrong(wa.feedback)
        except TestPassed as _:
            result = correct()
        except (TestedProgramThrewException, TestedProgramFinishedEarly) as _:
            result = None

        if result is None or result.is_correct:
            test_run.stop_tested_programs()

        return result

    def _run_file(self, test_run: TestRun) -> Optional[CheckResult]:
        test_case = test_run.test_case
        time_limit = test_case.time_limit

        executor = DaemonThreadPoolExecutor(name=f"AsyncMainFileRunner test #{test_run.test_num}")
        try:
            future: Future = executor.submit(lambda: self._run_dynamic_test(test_run))
            if time_limit <= 0 or debug_mode:
                return future.result()
            else:
                return future.result(timeout=time_limit / 1000)
        except TimeoutError:
            test_run.set_error_in_test(TimeLimitException(time_limit))
        except BaseException as ex:
            test_run.set_error_in_test(ex)
        finally:
            executor.shutdown(wait=False)

        return None

    def test(self, test_run: TestRun) -> Optional[CheckResult]:
        test_case = test_run.test_case

        result: CheckResult = self._run_file(test_run)

        if result is None:
            error = test_run.error_in_test

            if error is None:
                try:
                    return test_case.check_func(
                        OutputHandler.get_output(), test_case.attach)
                except BaseException as ex:
                    error = ex
                    test_run.set_error_in_test(error)

            if isinstance(error, TestPassed):
                return correct()
            elif isinstance(error, WrongAnswer):
                return wrong(error.feedback)
            else:
                return None

        return result
