import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


@unittest.skip("Relative imports doesn't work")
class TestImportRelativeError(UserErrorTest):
    contain = """
        Error in test #1
    
        Traceback (most recent call last):
          File "main.py", line 1, in <module>
            from .main22 import x
        ModuleNotFoundError: No module named 'tests.outcomes.imports.test_import_relative_error.main22'
        """  # noqa: W293, E501

    def generate(self) -> List[TestCase]:
        return [TestCase()]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == "1036\n", "")
