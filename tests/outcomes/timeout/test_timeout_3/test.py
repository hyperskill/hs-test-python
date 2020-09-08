import unittest
import os
from inspect import cleandoc
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestTimeout3(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(time_limit=2000),
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult.correct()


@unittest.skip
class Test(unittest.TestCase):
    def test(self):
        file = __file__.replace(os.sep, '.')[:-3]
        file = file[file.find('.tests.') + 1: file.rfind('.') + 1] + 'main'
        status, feedback = TestTimeout3(file).run_tests()

        self.assertTrue("Error in test #1" in feedback)
        self.assertTrue(
            "In this test, " +
            "the program is running for a long time, more than 2 seconds. " +
            "Most likely, the program has gone into an infinite loop." in feedback)

        self.assertTrue("Fatal error" not in feedback)

        self.assertNotEqual(status, 0)
