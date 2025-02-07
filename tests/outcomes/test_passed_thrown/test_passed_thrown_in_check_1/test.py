from typing import Any, List

from hstest.check_result import CheckResult
from hstest.exceptions import TestPassed
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestPassedThrownInCheck1(UserErrorTest):
    contain = """
    Wrong answer in test #1

    test is not passed attach true"""

    def generate(self) -> List[TestCase]:
        return [TestCase(attach=True), TestCase(attach=False)]

    def check(self, reply: str, attach: Any) -> CheckResult:
        if not attach:
            raise TestPassed("Wrong answer from check attach true")
        return CheckResult(False, "test is not passed attach true")
