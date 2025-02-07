import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


@unittest.skip("takes too loong")
class TestDefaultTimeLimit(UserErrorTest):
    contain = [
        "Error in test #1",
        "In this test, the program is running for a long time, more than 15 seconds. "
        "Most likely, the program has gone into an infinite loop.",
    ]

    def generate(self) -> List[TestCase]:
        return [TestCase()]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult.correct()
