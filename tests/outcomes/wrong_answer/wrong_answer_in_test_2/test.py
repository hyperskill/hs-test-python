from typing import Any, List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


class WrongAnswerInTest2(UserErrorTest):
    contain = "Wrong answer in test #2"

    def generate(self) -> List[TestCase]:
        return [
            TestCase(attach=True),
            TestCase(attach=False)
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(attach, '')
