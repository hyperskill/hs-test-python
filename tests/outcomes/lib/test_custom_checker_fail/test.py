from typing import Any, List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.unexepected_error_test import UnexpectedErrorTest


class TestCustomChecker(UnexpectedErrorTest):
    contain = [
        "Unexpected error in test #2",
        "UnexpectedError: Can't ",
        'check result: override "check" method',
    ]

    def generate(self) -> List[TestCase]:
        return [
            TestCase(
                attach="4\n-in\n123\nout\n234\n",
                args=["-in", "123", "out", "234"],
                check_function=self.custom_check,
            ),
            TestCase(
                attach="5\n-in\n435\nout\n567\n789\n",
                args=["-in", "435", "out", "567", "789"],
            ),
        ]

    def custom_check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == attach, "")
