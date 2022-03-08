import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class WrongAnswerDynamicInput3(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin=[
                (-1, lambda x: CheckResult.correct())
            ], attach="1\n2\n2\n"),

            TestCase(stdin=[
                lambda x: CheckResult.correct() if x == "" else CheckResult.wrong("WA TEST 2"),
                (2, lambda x: CheckResult.correct() if x == "3\n" else CheckResult.wrong("WA TEST 2"))
            ], attach="3\n3\n3\n"),

            TestCase(stdin=[
                lambda x: "3" if x == "" else CheckResult.wrong("WA TEST 3"),
                (-1, lambda x: "4" if x == "3\n" else CheckResult.wrong("WA TEST 3"))
            ], attach="3\n3\n4\n"),
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == attach, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = WrongAnswerDynamicInput3(source_name='main').run_tests()

        self.assertTrue("Wrong answer in test #3" in feedback)
        self.assertTrue("WA TEST 3" in feedback)

        self.assertTrue("Fatal error" not in feedback)

        self.assertNotEqual(status, 0)
