from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestCaseSameObjects(StageTest):

    def generate(self) -> List[TestCase]:
        test = TestCase(stdin=[(3, lambda x: x)], attach="Hello\nHello\nHello\nHello\n")
        return [test] * 5

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == attach, "")
