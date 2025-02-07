from typing import Any, List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


class ExceptionInUserCodeTest(UserErrorTest):
    contain = """
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
    """  # noqa: W293

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin="2\n4", attach="6\n"),
            TestCase(stdin="1\n3", attach="4\n"),
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == attach, "")
