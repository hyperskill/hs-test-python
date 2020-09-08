import unittest
import os
from inspect import cleandoc
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
        file = __file__.replace(os.sep, '.')[:-3]
        file = file[file.find('.tests.') + 1: file.rfind('.') + 1] + 'main'
        status, feedback = WrongAnswerThrownInDynamicInput1(file).run_tests()

        self.assertTrue("Wrong answer in test #1\n\n"
                        "Add input test 1" in feedback)
        self.assertTrue("Fatal error" not in feedback)

        self.assertNotEqual(status, 0)
