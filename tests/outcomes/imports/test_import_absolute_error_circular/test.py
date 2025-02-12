from typing import Any, List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestImportAbsoluteErrorCircular(UserErrorTest):
    contain = """
            Exception in test #1

            Traceback (most recent call last):
              File "main.py", line 1, in <module>
                import main2
              File "main2.py", line 1, in <module>
                import main
              File "main.py", line 2, in <module>
                print(main2.x)
            """

    source = "main"

    def generate(self) -> List[TestCase]:
        return [TestCase()]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == "1040\n", "")
