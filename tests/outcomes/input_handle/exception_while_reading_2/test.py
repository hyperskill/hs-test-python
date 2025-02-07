from typing import Any, List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


class ExceptionWhileReading2(UserErrorTest):
    contain = """
    Error in test #1

    Program ran out of input. You tried to read more than expected.
    
    Please find below the output of your program during this failed test.
    Note that the '>' character indicates the beginning of the input line.
    
    ---
    
    > line1
    line1
    > line2
    line2"""  # noqa: W293

    def generate(self) -> List[TestCase]:
        return [TestCase(stdin="line1\nline2")]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, "")
