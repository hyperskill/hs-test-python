from typing import Any, List

from hstest.check_result import CheckResult
from hstest.exceptions import TestPassed
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestPassedThrownInDynamicInput1(UserErrorTest):
    contain = """
    Wrong answer in test #2

    fail inside check
    """

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin=[self.dynamic1]),
            TestCase(stdin=[self.dynamic2])
        ]

    def dynamic1(self, out):
        if out == '1':
            raise TestPassed()
        return '2'

    def dynamic2(self, out):
        if out == '2':
            raise TestPassed()
        return '1'

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult.wrong("fail inside check")
