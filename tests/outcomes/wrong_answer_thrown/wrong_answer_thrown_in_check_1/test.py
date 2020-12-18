import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.exceptions import WrongAnswer
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class WrongAnswerThrownInCheck1(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(attach=True),
            TestCase(attach=False)
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        if not attach:
            raise WrongAnswer("Wrong answer from check attach false")
        return CheckResult(attach, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = WrongAnswerThrownInCheck1('main').run_tests()

        self.assertTrue("Wrong answer in test #2\n\n"
                        "Wrong answer from check attach false" in feedback)
        self.assertTrue("Fatal error" not in feedback)

        self.assertNotEqual(status, 0)
