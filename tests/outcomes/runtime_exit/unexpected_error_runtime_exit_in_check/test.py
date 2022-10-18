from typing import Any, List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.unexepected_error_test import UnexpectedErrorTest


class UnexpectedErrorRuntimeExitInCheck(UnexpectedErrorTest):
    contain = [
        """
        Unexpected error in test #1
        
        We have recorded this bug and will fix it soon.
        """,  # noqa: W293
        'ExitException'
    ]

    def generate(self) -> List[TestCase]:
        return [
            TestCase()
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        quit(0)
        return CheckResult(True, '')
