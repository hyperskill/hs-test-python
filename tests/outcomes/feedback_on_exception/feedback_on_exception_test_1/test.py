from typing import Any, List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


class FeedbackOnExceptionTest1(UserErrorTest):
    contain = """
    Exception in test #1

    Do not divide by zero!
    
    Traceback (most recent call last):
      File "main.py", line 2, in <module>
        print(1 / 0)
    ZeroDivisionError: division by zero
    
    Please find below the output of your program during this failed test.
    
    ---
    
    Hello World
    """  # noqa: W293

    def generate(self) -> List[TestCase]:
        return [
            TestCase(feedback_on_exception={
                ZeroDivisionError: 'Do not divide by zero!'
            })
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, '')
