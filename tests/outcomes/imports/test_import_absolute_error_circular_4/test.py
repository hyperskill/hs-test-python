from typing import Any, List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestImportAbsoluteErrorCircular4(UserErrorTest):
    contain = """
            Error in test #1

            Cannot decide which file to run out of the following: "main.py", "main2.py"
            Write "if __name__ == '__main__'" in one of them to mark it as an entry point.
            """

    def generate(self) -> List[TestCase]:
        return [TestCase()]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == "107\n", "")
