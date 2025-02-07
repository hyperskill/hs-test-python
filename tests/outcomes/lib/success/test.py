from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class SuccessTest(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin="2\n4", attach="6\n"),
            TestCase(stdin="1\n3", attach="4\n"),
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == attach, "")
