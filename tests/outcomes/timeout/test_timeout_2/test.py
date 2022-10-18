import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


@unittest.skip('takes too long')
class TestTimeout2(UserErrorTest):
    contain = [
        'Error in test #3',
        'In this test, the program is running for a long time, more than 300 milliseconds. '
        'Most likely, the program has gone into an infinite loop.'
    ]

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin="100", time_limit=300),
            TestCase(stdin="200", time_limit=300),
            TestCase(stdin="400", time_limit=300),
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult.correct()
