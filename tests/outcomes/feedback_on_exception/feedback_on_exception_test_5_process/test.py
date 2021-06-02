import unittest
from inspect import cleandoc
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class FeedbackOnExceptionTest5(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(feedback_on_exception={
                AttributeError: 'Attribute Error raised!',
                Exception: 'Base ex raised'
            })
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = FeedbackOnExceptionTest5('main').run_tests()

        self.assertEqual(cleandoc('''\
            Exception in test #1
            
            Traceback (most recent call last):
              File "main.py", line 1, in <module>
                raise ZeroDivisionError()
            ZeroDivisionError'''), feedback)

        self.assertEqual(status, -1)


if __name__ == '__main__':
    Test().test()
