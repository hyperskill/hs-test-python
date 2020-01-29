import unittest
import textwrap
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class FeedbackOnExceptionTest1(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(feedback_on_exception={
                ZeroDivisionError: 'Do not divide by zero!'
            })
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = FeedbackOnExceptionTest1(
            'tests.outcomes.feedback_on_exception_test_1.program'
        ).run_tests()

        self.assertEqual(textwrap.dedent('''\
            Exception in test #1
            
            Do not divide by zero!
            
            Traceback (most recent call last):
              File "program.py", line 2, in <module>
                print(1 / 0)
            ZeroDivisionError: division by zero
            
            Please find below the output of your program during this failed test.
            
            ---
            
            Hello World'''), feedback)

        self.assertEqual(status, -1)
