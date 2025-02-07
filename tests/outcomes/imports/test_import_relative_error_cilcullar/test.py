import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


@unittest.skip("Relative imports doesn't work")
class TestImportRelativeErrorCircular(UserErrorTest):
    contain = """
            Error in test #1

            Traceback (most recent call last):
              File "main.py", line 1, in <module>
                from .main2 import x
              File "main2.py", line 1, in <module>
                from .main import y
              File "main.py", line 1, in <module>
                from .main2 import x
            ImportError: cannot import name 'x' from partially initialized module 
            """  # noqa: W291

    def generate(self) -> List[TestCase]:
        return [TestCase()]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == "1038\n", "")
