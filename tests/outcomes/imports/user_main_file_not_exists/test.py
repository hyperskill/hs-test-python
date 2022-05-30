from typing import Any, List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


class UnexpectedErrorUserMainFileNotExists(UserErrorTest):
    contain = """
    Error in test #1
    
    Cannot find a file to execute your code.
    Are your project files located at 
    """

    def generate(self) -> List[TestCase]:
        return [TestCase()]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, '')
