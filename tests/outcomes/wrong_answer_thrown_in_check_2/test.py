import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.exceptions import WrongAnswer
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class WrongAnswerThrownInCheck2(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(attach=True),
            TestCase(attach=False)
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        if attach:
            raise WrongAnswer("Wrong answer from check attach true")
        return CheckResult(attach, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = WrongAnswerThrownInCheck2(
            'tests.outcomes.wrong_answer_thrown_in_check_2.program'
        ).run_tests()

        self.assertTrue("Wrong answer in test #1\n\n"
                        "Wrong answer from check attach true" in feedback)
        self.assertTrue("Fatal error" not in feedback)

        self.assertNotEqual(status, 0)
