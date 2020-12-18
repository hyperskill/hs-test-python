import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class WrongAnswerDynamicInput1(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin=[lambda x: CheckResult.wrong("WA TEST 1")]),
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult.wrong('')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = WrongAnswerDynamicInput1('main').run_tests()

        self.assertTrue("Wrong answer in test #1" in feedback)
        self.assertTrue("WA TEST 1" in feedback)

        self.assertTrue("Fatal error" not in feedback)

        self.assertNotEqual(status, 0)
