import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.common.reflection_utils import get_main
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
        status, feedback = TestPassedThrownInCheck2(get_main()).run_tests()

        self.assertTrue("Wrong answer in test #2\n\n"
                        "test is not passed attach false" in feedback)
        self.assertTrue("Fatal error" not in feedback)

        self.assertNotEqual(status, 0)
