from typing import Any

from hstest.check_result import CheckResult
from testing.unittest.unexepected_error_test import UnexpectedErrorTest


class UnexpectedErrorGeneratingTestsWithAssertion(UnexpectedErrorTest):
    contain = [
        """
        Unexpected error during testing

        We have recorded this bug and will fix it soon.
        """
    ]

    def generate(self):
        assert False

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, '')
