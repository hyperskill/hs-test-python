import unittest
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
        status, feedback = ExceptionWhileReading2('main').run_tests()

        self.assertEqual(status, -1)
        self.assertTrue('Exception in test #1' in feedback)
        self.assertTrue('Probably your program run out of input' in feedback)
        self.assertTrue('Traceback (most recent call last):' in feedback)
        self.assertTrue('    print(input())' in feedback)
        self.assertTrue('EOFError: EOF when reading a line' in feedback)
