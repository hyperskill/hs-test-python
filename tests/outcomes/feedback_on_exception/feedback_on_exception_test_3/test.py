import unittest
from inspect import cleandoc
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class FeedbackOnExceptionTest3(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(feedback_on_exception={
                ZeroDivisionError: 'Do not divide by zero!',
                AttributeError: 'Attribute Error raised!'
            })
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = FeedbackOnExceptionTest3().run_tests()

        self.assertEqual(cleandoc('''\
            Exception in test #1
            
            Traceback (most recent call last):
              File "main.py", line 1, in <module>
                raise Exception()
            Exception'''), feedback)

        self.assertEqual(status, -1)


if __name__ == '__main__':
    Test().test()
