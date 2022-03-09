import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class WrongAnswerDynamicInput4(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin=[
                "1",
                (2, lambda x: CheckResult.correct())
            ], attach="1\n2\n2\n"),

            TestCase(stdin=[
                (2, lambda x: "3"),
                lambda x: "3",
                lambda x: CheckResult.wrong("WA TEST 2")
            ], attach="3\n3\n3\n"),

            TestCase(stdin=[
                (-1, lambda x: "4"),
                lambda x: CheckResult.wrong("WA TEST 3")
            ], attach="4\n4\n4\n"),

            TestCase(stdin=[
                (2, lambda x: "5"),
                lambda x: CheckResult.wrong("WA TEST 4") if x == "5\n" else 5
            ], attach="4\n4\n4\n"),
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == attach, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = WrongAnswerDynamicInput4().run_tests()

        self.assertTrue("Wrong answer in test #4" in feedback)
        self.assertTrue("WA TEST 4" in feedback)

        self.assertTrue("Fatal error" not in feedback)

        self.assertNotEqual(status, 0)
