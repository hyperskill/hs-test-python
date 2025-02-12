import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


@unittest.skip("takes too long")
class TestTimeout1(UserErrorTest):
    contain = [
        "Error in test #2",
        "In this test, the program is running for a long time, more than 500 milliseconds. "
        "Most likely, the program has gone into an infinite loop.",
    ]

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin="400", time_limit=500),
            TestCase(stdin="600", time_limit=500),
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult.correct()
