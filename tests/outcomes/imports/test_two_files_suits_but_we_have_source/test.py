from typing import Any, List

from hstest import CheckResult, correct, TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestImportRelativeError2(UserErrorTest):
    contain = """
            Error in test #1

            Cannot decide which file to run out of the following: "main1.py", "main2.py"
            Write "if __name__ == '__main__'" in one of them to mark it as an entry point.
            """

    def generate(self) -> List[TestCase]:
        return [TestCase()]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return correct()
