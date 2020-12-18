import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.exceptions import TestPassed
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestPassedThrownInDynamicInput2(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin=[self.dynamic1]),
            TestCase(stdin=[self.dynamic2])
        ]

    def dynamic1(self, out):
        if out == '1':
            raise TestPassed()
        return '2'

    def dynamic2(self, out):
        if out == '2':
            raise TestPassed()
        return '1'

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult.wrong("fail inside check")


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestPassedThrownInDynamicInput2('main').run_tests()

        self.assertTrue("Wrong answer in test #1\n\n"
                        "fail inside check" in feedback)
        self.assertTrue("Fatal error" not in feedback)

        self.assertNotEqual(status, 0)
