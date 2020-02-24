import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestDynamicOutputWithInput(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin="123 456\n678\n248")
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult.wrong('')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestDynamicOutputWithInput(
            'tests.outcomes.test_dynamic_output_with_input.program'
        ).run_tests()

        self.assertTrue('Wrong answer in test #1' in feedback)
        self.assertTrue(
            "Please find below the output of your program during this failed test.\n" +
            "Note that the '>' character indicates the beginning of the input line.\n" +
            "\n---\n\n" +
            "Print x and y: > 123 456\n" +
            "> 678\n" +
            "Another num:\n" +
            "> 248" in feedback
        )

        self.assertTrue("Fatal error" not in feedback)

        self.assertNotEqual(status, 0)
