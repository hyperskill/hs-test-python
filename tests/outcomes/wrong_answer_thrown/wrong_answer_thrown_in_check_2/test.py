from typing import Any, List

from hstest.check_result import CheckResult
from hstest.exceptions import WrongAnswer
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


class WrongAnswerThrownInCheck2(UserErrorTest):
    contain = """
    Wrong answer in test #1

    Wrong answer from check attach true
    """

    def generate(self) -> List[TestCase]:
        return [TestCase(attach=True), TestCase(attach=False)]

    def check(self, reply: str, attach: Any) -> CheckResult:
        if attach:
            raise WrongAnswer("Wrong answer from check attach true")
        return CheckResult(attach, "")
