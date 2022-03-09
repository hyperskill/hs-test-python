import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class WrongAnswerDynamicInput2(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin=[
                lambda x: "2" if x == "1\n" else CheckResult.wrong("WA TEST 1")
            ], attach="1\n2\n"),

            TestCase(stdin=[
                lambda x: "3" if x == "2" else CheckResult.wrong("WA TEST 2")
            ], attach="2\n3\n"),
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == attach, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = WrongAnswerDynamicInput2().run_tests()

        self.assertTrue("Wrong answer in test #2" in feedback)
        self.assertTrue("WA TEST 2" in feedback)

        self.assertTrue("Fatal error" not in feedback)

        self.assertNotEqual(status, 0)
