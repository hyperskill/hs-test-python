from typing import Any, List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


class SearchGoFileTest(UserErrorTest):
    contain = """
    Cannot decide which file to run out of the following: "another.go", "main.go"
    They all have ['package main', 'func main()']. Leave one file with this lines.
    """  # noqa: W293, W291

    def generate(self) -> List[TestCase]:
        return [TestCase()]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, "")
