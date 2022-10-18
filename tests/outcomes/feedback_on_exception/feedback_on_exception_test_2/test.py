from typing import Any, List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


class FeedbackOnExceptionTest2(UserErrorTest):
    contain = '''
        Exception in test #1
        
        Attribute Error raised!
        
        Traceback (most recent call last):
          File "main.py", line 1, in <module>
            raise AttributeError()
        AttributeError'''  # noqa: W293

    def generate(self) -> List[TestCase]:
        return [
            TestCase(feedback_on_exception={
                ZeroDivisionError: 'Do not divide by zero!',
                AttributeError: 'Attribute Error raised!'
            })
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, '')
