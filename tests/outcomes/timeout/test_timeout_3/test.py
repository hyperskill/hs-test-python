import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


@unittest.skip('take too long')
class TestTimeout3(UserErrorTest):
    contain = [
        'Error in test #1',
        'In this test, the program is running for a long time, more than 2 seconds. '
        'Most likely, the program has gone into an infinite loop.'
    ]

    def generate(self) -> List[TestCase]:
        return [
            TestCase(time_limit=2000),
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult.correct()
