from typing import Any, List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.unexepected_error_test import UnexpectedErrorTest


class UnexpectedErrorAddInput1(UnexpectedErrorTest):
    contain = [
        """
        Unexpected error in test #1

        We have recorded this bug and will fix it soon.
        """,
        "ZeroDivisionError: division by zero",
    ]

    def generate(self) -> List[TestCase]:
        return [TestCase(stdin=[lambda x: f"{0 / 0}"])]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, "")
