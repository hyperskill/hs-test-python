from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestNbspInOutput(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase()
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == "1\u00202\u00203", '')
