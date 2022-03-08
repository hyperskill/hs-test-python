import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class WrongAnswerInTest2(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(attach=True),
            TestCase(attach=False)
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(attach, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = WrongAnswerInTest2(source_name='main').run_tests()

        self.assertTrue("Wrong answer in test #2" in feedback)
        self.assertTrue("Fatal error" not in feedback)

        self.assertNotEqual(status, 0)
