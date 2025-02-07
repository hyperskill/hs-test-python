from typing import Any

from hstest.check_result import CheckResult
from hstest.testing.unittest.unexepected_error_test import UnexpectedErrorTest


class UnexpectedErrorNotGeneratingTests(UnexpectedErrorTest):
    contain = [
        """
        Unexpected error during testing

        We have recorded this bug and will fix it soon.
        """,
        "No tests found",
    ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, "")
