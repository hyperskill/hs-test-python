import unittest
import os
from inspect import cleandoc
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class ExceptionWhileReading2(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin='line1\nline2')
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, '')


class Test(unittest.TestCase):
    def test(self):
        file = __file__.replace(os.sep, '.')[:-3]
        file = file[file.find('.tests.') + 1: file.rfind('.') + 1] + 'main'
        status, feedback = ExceptionWhileReading2(file).run_tests()

        self.assertEqual(status, -1)
        self.assertTrue('Exception in test #1' in feedback)
        self.assertTrue('Probably your program run out of input' in feedback)
        self.assertTrue('Traceback (most recent call last):' in feedback)
        self.assertTrue('    print(input())' in feedback)
        self.assertTrue('EOFError: EOF when reading a line' in feedback)
