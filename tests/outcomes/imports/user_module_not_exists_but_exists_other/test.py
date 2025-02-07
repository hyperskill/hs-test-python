from typing import Any, List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


class UnexpectedErrorUserModuleNotExistsButExistsOther(UserErrorTest):
    contain = """
    Error in test #1

    Cannot find a file to execute your code.
    Are your project files located at
    """

    source = "tests.bad_module"

    def generate(self) -> List[TestCase]:
        return [TestCase()]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, "")
