from typing import Any, List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestOutOfInput4(UserErrorTest):
    contain = """
    Error in test #1

    Program ran out of input. You tried to read more than expected.
    """

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin=[(2, lambda x: '1\n2'),
                            lambda x: '2'])
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult.correct()
