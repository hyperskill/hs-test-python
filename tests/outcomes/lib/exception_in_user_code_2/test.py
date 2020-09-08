import unittest
import os
from inspect import cleandoc
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
        file = __file__.replace(os.sep, '.')[:-3]
        file = file[file.find('.tests.') + 1: file.rfind('.') + 1] + 'main'
        status, feedback = ExceptionInUserCodeTest(file).run_tests()

        self.assertEqual(cleandoc(
            """
            Exception in test #1
            
            Traceback (most recent call last):
              File "main.py", line 3, in <module>
                print(0 / 0)
              File "main.py", line 5, in <module>
                print(0 / 0)
            ZeroDivisionError: division by zero
            
            Please find below the output of your program during this failed test.
            
            ---
            
            123
            """), feedback)


if __name__ == '__main__':
    Test().test()
