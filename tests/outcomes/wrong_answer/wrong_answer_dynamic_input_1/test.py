from typing import Any, List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


class WrongAnswerDynamicInput1(UserErrorTest):
    contain = """
    Wrong answer in test #1

    WA TEST 1
    """

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin=[lambda x: CheckResult.wrong("WA TEST 1")]),
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult.wrong("")
