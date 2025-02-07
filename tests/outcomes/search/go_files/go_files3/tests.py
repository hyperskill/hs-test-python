from typing import Any, List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


class SearchGoFileTest(UserErrorTest):
    contain = """
    The runnable file should contain all the following lines: ['package main', 'func main()']
    """  # noqa: W293, W291

    def generate(self) -> List[TestCase]:
        return [TestCase()]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, "")
