from typing import Any, List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


class WrongAnswerDynamicInput3(UserErrorTest):
    contain = """
    Wrong answer in test #3

    WA TEST 3
    """

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin=[
                (-1, lambda x: CheckResult.correct())
            ], attach="1\n2\n2\n"),

            TestCase(stdin=[
                lambda x: CheckResult.correct() if x == "" else CheckResult.wrong("WA TEST 2"),
                (2, lambda x: CheckResult.correct() if x == "3\n" else CheckResult.wrong("WA TEST 2"))
            ], attach="3\n3\n3\n"),

            TestCase(stdin=[
                lambda x: "3" if x == "" else CheckResult.wrong("WA TEST 3"),
                (-1, lambda x: "4" if x == "3\n" else CheckResult.wrong("WA TEST 3"))
            ], attach="3\n3\n4\n"),
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == attach, '')
