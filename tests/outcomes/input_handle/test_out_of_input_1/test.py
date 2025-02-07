from typing import Any, List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestOutOfInput1(UserErrorTest):
    contain = """
    Error in test #1

    Program ran out of input. You tried to read more than expected.
    
    Please find below the output of your program during this failed test.
    Note that the '>' character indicates the beginning of the input line.
    
    ---
    
    > 1
    1
    > 2
    2
    > 3
    3
    > 4
    4
    > 5
    5"""  # noqa: W293

    def generate(self) -> List[TestCase]:
        return [
            TestCase(
                stdin=[
                    lambda x: "1",
                    lambda x: "2",
                    lambda x: "3",
                    lambda x: "4",
                    lambda x: "5",
                ]
            )
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult.correct()
