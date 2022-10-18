from typing import Any, List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


class ExceptionInUserCodeTest3(UserErrorTest):
    contain = """
            Exception in test #1

            Traceback (most recent call last):
              File "main.py", line 2, in <module>
                Coffee is ready!\"\"\", raise_error_here)
            NameError: name 'raise_error_here' is not defined
            """

    def generate(self) -> List[TestCase]:
        return [TestCase()]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult.correct()
