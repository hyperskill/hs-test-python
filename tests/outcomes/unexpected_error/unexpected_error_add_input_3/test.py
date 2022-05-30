from typing import Any, List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.unexepected_error_test import UnexpectedErrorTest


class UnexpectedErrorAddInput3(UnexpectedErrorTest):
    contain = [
        """
        Unexpected error in test #4

        We have recorded this bug and will fix it soon.
        """,
        "Dynamic input should return str or CheckResult objects only. Found: <class 'int'>"
    ]

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin=['12'], attach='1\n12\n'),
            TestCase(stdin=[lambda x: CheckResult.correct()]),
            TestCase(stdin=[lambda x: CheckResult(x == '1\n', x + '56')]),
            TestCase(stdin=[lambda x: 78])
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, '')
