from typing import Any, List

from hstest.check_result import CheckResult
from hstest.exceptions import WrongAnswer
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


class WrongAnswerThrownInCheck1(UserErrorTest):
    contain = """
    Wrong answer in test #2

    Wrong answer from check attach false
    """

    def generate(self) -> List[TestCase]:
        return [TestCase(attach=True), TestCase(attach=False)]

    def check(self, reply: str, attach: Any) -> CheckResult:
        if not attach:
            raise WrongAnswer("Wrong answer from check attach false")
        return CheckResult(attach, "")
