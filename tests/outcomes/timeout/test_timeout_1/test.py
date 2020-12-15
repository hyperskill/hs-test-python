import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.common.reflection_utils import get_main
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestTimeout1(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin="400", time_limit=500),
            TestCase(stdin="600", time_limit=500)
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult.correct()


@unittest.skip
class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestTimeout1(get_main()).run_tests()

        self.assertTrue("Error in test #2" in feedback)
        self.assertTrue(
            "In this test, " +
            "the program is running for a long time, more than 500 milliseconds. " +
            "Most likely, the program has gone into an infinite loop." in feedback)

        self.assertTrue("Fatal error" not in feedback)

        self.assertNotEqual(status, 0)
