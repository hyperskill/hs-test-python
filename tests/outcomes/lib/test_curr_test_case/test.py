import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestCurrTestCase(StageTest):
    tc_1 = None
    tc_2 = None

    def generate(self) -> List[TestCase]:
        self.tc_1 = TestCase(stdin='1', attach=1)
        self.tc_2 = TestCase(stdin='2', attach=2)
        return [self.tc_1, self.tc_2]

    def check(self, reply: str, attach: Any) -> CheckResult:
        tc = StageTest.curr_test_run.test_case
        if (tc.input == '1' and tc.attach == 1 and tc is self.tc_1 or
                tc.input == '2' and tc.attach == 2 and tc is self.tc_2):
            return CheckResult.correct()
        return CheckResult.wrong('')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestCurrTestCase().run_tests()
        self.assertEqual('test OK', feedback)
        self.assertEqual(status, 0)
