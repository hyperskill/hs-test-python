import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestTimeout2(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin="100", time_limit=300),
            TestCase(stdin="200", time_limit=300),
            TestCase(stdin="400", time_limit=300),
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult.correct()


@unittest.skip
class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestTimeout2(source_name='main').run_tests()

        self.assertTrue("Error in test #3" in feedback)
        self.assertTrue(
            "In this test, " +
            "the program is running for a long time, more than 300 milliseconds. " +
            "Most likely, the program has gone into an infinite loop." in feedback)

        self.assertTrue("Fatal error" not in feedback)

        self.assertNotEqual(status, 0)
