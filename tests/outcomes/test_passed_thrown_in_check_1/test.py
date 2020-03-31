import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.exceptions import TestPassed
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestPassedThrownInCheck1(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(attach=True),
            TestCase(attach=False)
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        if not attach:
            raise TestPassed("Wrong answer from check attach true")
        return CheckResult(False, "test is not passed attach true")


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestPassedThrownInCheck1(
            'tests.outcomes.test_passed_thrown_in_check_1.program'
        ).run_tests()

        self.assertTrue("Wrong answer in test #1\n\n"
                        "test is not passed attach true" in feedback)
        self.assertTrue("Fatal error" not in feedback)

        self.assertNotEqual(status, 0)
