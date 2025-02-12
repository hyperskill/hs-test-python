from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestDynamicOutput(StageTest):

    def generate(self) -> List[TestCase]:
        return [TestCase(stdin=[self.in1, self.in2])]

    def in1(self, out):
        if out != "1\n2\n":
            0 / 0
        return "3\n4"

    def in2(self, out):
        if out != "5\n6\n":
            0 / 0
        return "7\n8\n"

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult.correct()
