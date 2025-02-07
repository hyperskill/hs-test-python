from typing import Any, List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


class WrongAnswerDynamicInput2(UserErrorTest):
    contain = """
    Wrong answer in test #2

    WA TEST 2
    """

    def generate(self) -> List[TestCase]:
        return [
            TestCase(
                stdin=[lambda x: "2" if x == "1\n" else CheckResult.wrong("WA TEST 1")],
                attach="1\n2\n",
            ),
            TestCase(
                stdin=[lambda x: "3" if x == "2" else CheckResult.wrong("WA TEST 2")],
                attach="2\n3\n",
            ),
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == attach, "")
