import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.exceptions import TestPassed
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestPassedThrownInCheck2(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(attach=True),
            TestCase(attach=False)
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        if attach:
            raise TestPassed()
        return CheckResult(False, "test is not passed attach false")


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestPassedThrownInCheck2(
            'tests.outcomes.test_passed_thrown_in_check_2.program'
        ).run_tests()

        self.assertTrue("Wrong answer in test #2\n\n"
                        "test is not passed attach false" in feedback)
        self.assertTrue("Fatal error" not in feedback)

        self.assertNotEqual(status, 0)
