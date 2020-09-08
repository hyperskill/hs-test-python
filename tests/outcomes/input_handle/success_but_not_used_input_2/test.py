import unittest
import os
from inspect import cleandoc
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class SuccessButNotUsedInput2(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin=[self.add_input], attach='NO')
        ]

    def add_input(self, out: str):
        if out == 'HELLO\n':
            return CheckResult.correct()
        return ''

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult.correct()


class Test(unittest.TestCase):
    def test(self):
        file = __file__.replace(os.sep, '.')[:-3]
        file = file[file.find('.tests.') + 1: file.rfind('.') + 1] + 'main'
        status, feedback = SuccessButNotUsedInput2(file).run_tests()
        self.assertEqual(feedback, 'test OK')
        self.assertEqual(status, 0)
