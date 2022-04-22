from typing import Any, List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.unexepected_error_test import UnexpectedErrorTest


class UnexpectedErrorGeneratingTests(UnexpectedErrorTest):
    contain = [
        """
        Unexpected error during testing

        We have recorded this bug and will fix it soon.
        """
    ]

    def generate(self) -> List[TestCase]:
        x = 0 / 0
        return [
            TestCase()
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, '')
