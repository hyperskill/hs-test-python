import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.exceptions import WrongAnswer
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class WrongAnswerThrownInDynamicInput1(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin=[self.dynamic1]),
            TestCase(stdin=[self.dynamic2])
        ]

    def dynamic1(self, out):
        if out == '1':
            raise WrongAnswer("Add input test 1")
        return '2'

    def dynamic2(self, out):
        if out == '2':
            raise WrongAnswer("Add input test 2")
        return '1'

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult.correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = WrongAnswerThrownInDynamicInput1(
            'tests.outcomes.wrong_answer_thrown_in_dynamic_input_1.program'
        ).run_tests()

        self.assertTrue("Wrong answer in test #1\n\n"
                        "Add input test 1" in feedback)
        self.assertTrue("Fatal error" not in feedback)

        self.assertNotEqual(status, 0)
