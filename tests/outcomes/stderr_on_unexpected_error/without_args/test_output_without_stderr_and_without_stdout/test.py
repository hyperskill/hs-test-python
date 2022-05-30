from typing import List, Any

from hstest import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestOutputWithStderrAndWithStdout(UserErrorTest):
    not_contain = [
        'stderr:',
        'stdout:'
    ]

    def generate(self) -> List[TestCase]:
        return [
            TestCase()
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult.wrong('')
