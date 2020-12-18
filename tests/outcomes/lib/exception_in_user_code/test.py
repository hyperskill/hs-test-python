import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class ExceptionInUserCodeTest(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin='2\n4', attach='6\n'),
            TestCase(stdin='1\n3', attach='4\n'),
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == attach, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = ExceptionInUserCodeTest('main').run_tests()
        self.assertEqual(status, -1)
        self.assertTrue('Exception in test #1' in feedback)
        self.assertTrue('Traceback (most recent call last):' in feedback)
        self.assertTrue(r'  File "main.py", line 2' in feedback)
        self.assertTrue('    print(0 / 0)' in feedback)
        self.assertTrue('ZeroDivisionError: division by zero' in feedback)


if __name__ == '__main__':
    Test().test()
