import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestCustomChecker(StageTest):
    def generate(self) -> List[TestCase]:
        return [
            TestCase(
                attach='4\n-in\n123\nout\n234\n',
                args=['-in', '123', 'out', '234'],
                check_function=self.custom_check
            ),
            TestCase(
                attach='5\n-in\n435\nout\n567\n789\n',
                args=['-in', '435', 'out', '567', '789']
            ),

        ]

    def custom_check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == attach, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestCustomChecker('main').run_tests()

        self.assertIn("Unexpected error in test #2", feedback)

        self.assertIn("UnexpectedError: Can't "
                      "check result: override \"check\" method", feedback)
        self.assertEqual(status, -1)
