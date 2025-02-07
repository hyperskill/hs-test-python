from typing import Any, List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


class FeedbackOnExceptionTest3(UserErrorTest):
    contain = """
    Exception in test #1

    Traceback (most recent call last):
      File "main.py", line 1, in <module>
        raise Exception()
    Exception
    """

    def generate(self) -> List[TestCase]:
        return [
            TestCase(
                feedback_on_exception={
                    ZeroDivisionError: "Do not divide by zero!",
                    AttributeError: "Attribute Error raised!",
                }
            )
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, "")
