import unittest
import os
from inspect import cleandoc
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
        file = __file__.replace(os.sep, '.')[:-3]
        file = file[file.find('.tests.') + 1: file.rfind('.') + 1] + 'main'
        status, feedback = WrongAnswerDynamicInput1(file).run_tests()

        self.assertTrue("Wrong answer in test #1" in feedback)
        self.assertTrue("WA TEST 1" in feedback)

        self.assertTrue("Fatal error" not in feedback)

        self.assertNotEqual(status, 0)
