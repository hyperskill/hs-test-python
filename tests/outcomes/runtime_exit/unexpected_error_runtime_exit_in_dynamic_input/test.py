from typing import Any, List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.unexepected_error_test import UnexpectedErrorTest


class UnexpectedErrorRuntimeExitInDynamicInput(UnexpectedErrorTest):
    contain = [
        """
        Unexpected error in test #3
        
        We have recorded this bug and will fix it soon.
        """,  # noqa: W293
        "ExitException"
    ]

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin=[lambda x: '123']),
            TestCase(stdin=[self.add_input_1]),
            TestCase(stdin=[self.add_input_2]),
        ]

    def add_input_1(self, stdin: str):
        return '123'

    def add_input_2(self, stdin: str):
        import sys
        sys.exit(0)
        return '123'

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, '')
