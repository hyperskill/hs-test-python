from typing import Any, List

from hstest import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestOutputWithStderrAndWithStdout(UserErrorTest):
    contain = "Arguments: test args"
    not_contain = ["stderr:", "stdout:"]

    def generate(self) -> List[TestCase]:
        return [TestCase(args=["test", "args"])]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult.wrong("")
