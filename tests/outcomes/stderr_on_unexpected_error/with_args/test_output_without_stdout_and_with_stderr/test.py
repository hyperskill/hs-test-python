from typing import Any, List

from hstest import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestOutputWithStderrAndWithStdout(UserErrorTest):
    contain = """
    Wrong answer in test #1

    Please find below the output of your program during this failed test.
    
    ---
    
    Arguments: test args
    
    stderr:
    User stderr output!
    User stderr output!
    User stderr output!"""  # noqa: W293

    def generate(self) -> List[TestCase]:
        return [
            TestCase(args=['test', 'args'])
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult.wrong('')
