import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestDefaultTimeLimit(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase()
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult.correct()


@unittest.skip
class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestDefaultTimeLimit('main').run_tests()

        self.assertTrue("Error in test #1" in feedback)
        self.assertTrue(
            "In this test, " +
            "the program is running for a long time, more than 15 seconds. " +
            "Most likely, the program has gone into an infinite loop." in feedback)

        self.assertTrue("Fatal error" not in feedback)

        self.assertNotEqual(status, 0)


if __name__ == '__main__':
    Test().test()
