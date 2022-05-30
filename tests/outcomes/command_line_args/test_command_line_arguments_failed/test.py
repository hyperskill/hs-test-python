from typing import Any, List

from hstest.check_result import CheckResult, wrong
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestCommandLineArgumentsFailed(UserErrorTest):
    contain = """
        Wrong answer in test #1

        Please find below the output of your program during this failed test.

        ---

        Arguments: -in 123 -out 234

        4
        -in
        123
        -out
        234
        """

    def generate(self) -> List[TestCase]:
        return [
            TestCase(args=["-in", "123", "-out", "234"])
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return wrong("")
