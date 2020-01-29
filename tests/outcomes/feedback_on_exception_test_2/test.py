import unittest
import textwrap
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class FeedbackOnExceptionTest2(StageTest):

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
        status, feedback = FeedbackOnExceptionTest2(
            'tests.outcomes.feedback_on_exception_test_2.program'
        ).run_tests()

        self.assertEqual(textwrap.dedent('''\
            Exception in test #1
            
            Attribute Error raised!
            
            Traceback (most recent call last):
              File "program.py", line 1, in <module>
                raise AttributeError()
            AttributeError'''), feedback)

        self.assertEqual(status, -1)
