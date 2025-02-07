from typing import Any, List

from hstest.check_result import CheckResult
from hstest.exceptions import TestPassed
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestPassedThrownInCheck2(UserErrorTest):
    contain = """
    Wrong answer in test #2
    
    test is not passed attach false
    """  # noqa: W293

    def generate(self) -> List[TestCase]:
        return [TestCase(attach=True), TestCase(attach=False)]

    def check(self, reply: str, attach: Any) -> CheckResult:
        if attach:
            raise TestPassed()
        return CheckResult(False, "test is not passed attach false")
