from typing import Any, List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


class WrongAnswerDynamicInput4(UserErrorTest):
    contain = """
    Wrong answer in test #4

    WA TEST 4
    """

    def generate(self) -> List[TestCase]:
        return [
            TestCase(
                stdin=["1", (2, lambda x: CheckResult.correct())], attach="1\n2\n2\n"
            ),
            TestCase(
                stdin=[
                    (2, lambda x: "3"),
                    lambda x: "3",
                    lambda x: CheckResult.wrong("WA TEST 2"),
                ],
                attach="3\n3\n3\n",
            ),
            TestCase(
                stdin=[(-1, lambda x: "4"), lambda x: CheckResult.wrong("WA TEST 3")],
                attach="4\n4\n4\n",
            ),
            TestCase(
                stdin=[
                    (2, lambda x: "5"),
                    lambda x: CheckResult.wrong("WA TEST 4") if x == "5\n" else 5,
                ],
                attach="4\n4\n4\n",
            ),
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == attach, "")
