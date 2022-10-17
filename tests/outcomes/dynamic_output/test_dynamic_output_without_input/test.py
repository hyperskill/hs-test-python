from typing import Any, List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestDynamicOutputWithoutInput(UserErrorTest):
    contain = [
        'Wrong answer in test #1',
        """
        Please find below the output of your program during this failed test.

        ---
        
        Print x and y: 123 456
        Another num:
        """  # noqa: W293
    ]

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin="123 456\n678\n248")
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult.wrong('')
