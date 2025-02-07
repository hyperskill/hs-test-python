from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestCurrTestNum(StageTest):
    tc_1 = None
    tc_2 = None

    def generate(self) -> List[TestCase]:
        self.tc_1 = TestCase(stdin="1", attach=1)
        self.tc_2 = TestCase(stdin="2", attach=2)
        return [self.tc_1, self.tc_2]

    def check(self, reply: str, attach: Any) -> CheckResult:
        tn = StageTest.curr_test_run.test_num
        if reply == "1\n" and tn == 1 or reply == "2\n" and tn == 2:
            return CheckResult.correct()
        return CheckResult.wrong("")
