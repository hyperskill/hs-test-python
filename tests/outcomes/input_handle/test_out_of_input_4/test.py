import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestOutOfInput4(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin=[(2, lambda x: '1\n2'),
                            lambda x: '2'])
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult.correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestOutOfInput4('main').run_tests()

        self.assertIn(
            "Error in test #1\n" +
            "\n" +
            "Program run out of input. You tried to read more, than expected.\n",
            feedback)

        self.assertTrue("Fatal error" not in feedback)

        self.assertNotEqual(status, 0)
