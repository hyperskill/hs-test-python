import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class ExceptionWhileReading2(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin='line1\nline2')
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = ExceptionWhileReading2().run_tests()

        self.assertEqual(status, -1)
        self.assertEqual(
            "Error in test #1\n" +
            "\n" +
            "Program ran out of input. You tried to read more than expected.\n" +
            "\n" +
            "Please find below the output of your program during this failed test.\n" +
            "Note that the '>' character indicates the beginning of the input line.\n" +
            "\n" +
            "---\n" +
            "\n" +
            "> line1\n" +
            "line1\n" +
            "> line2\n" +
            "line2",
            feedback)


if __name__ == '__main__':
    Test().test()
