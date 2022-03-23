import typing

from hstest.test_case.check_result import CheckResult
from hstest.testing.runner.test_runner import TestRunner

if typing.TYPE_CHECKING:
    from hstest.testing.test_run import TestRun


class SQLRunner(TestRunner):

    def test(self, test_run: 'TestRun'):
        test_case = test_run.test_case

        try:
            result = test_case.dynamic_testing()
            return result
        except BaseException as ex:
            test_run.set_error_in_test(ex)

        return CheckResult.from_error(test_run.error_in_test)
