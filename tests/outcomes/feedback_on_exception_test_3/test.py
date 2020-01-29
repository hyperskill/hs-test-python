import unittest
import textwrap
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
        status, feedback = FeedbackOnExceptionTest3(
            'tests.outcomes.feedback_on_exception_test_3.program'
        ).run_tests()

        self.assertEqual(textwrap.dedent('''\
            Exception in test #1
            
            Traceback (most recent call last):
              File "program.py", line 1, in <module>
                raise Exception()
            Exception'''), feedback)

        self.assertEqual(status, -1)
