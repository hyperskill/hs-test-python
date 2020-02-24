import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestNbspInOutput(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase()
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == "1 2 3", '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestNbspInOutput(
            'tests.outcomes.test_nbsp_in_output.program'
        ).run_tests()

        self.assertEqual("test OK", feedback)
        self.assertEqual(status, 0)
