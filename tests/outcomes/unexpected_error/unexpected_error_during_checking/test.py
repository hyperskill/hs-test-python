from typing import Any, List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from testing.unittest.unexepected_error_test import UnexpectedErrorTest


class UnexpectedErrorDuringChecking(UnexpectedErrorTest):
    contain = """
    Unexpected error in test #1

    We have recorded this bug and will fix it soon.
    """

    def generate(self) -> List[TestCase]:
        return [TestCase()]

    def check(self, reply: str, attach: Any) -> CheckResult:
        x = 0 / 0
        return CheckResult(True, '')
