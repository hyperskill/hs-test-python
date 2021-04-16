import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestOutOfInput1(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin=[lambda x: '1',
                            lambda x: '2',
                            lambda x: '3',
                            lambda x: '4',
                            lambda x: '5'])
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult.correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestOutOfInput1('main').run_tests()

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
            "> 1\n" +
            "1\n" +
            "> 2\n" +
            "2\n" +
            "> 3\n" +
            "3\n" +
            "> 4\n" +
            "4\n" +
            "> 5\n" +
            "5",
            feedback)

        self.assertTrue("Fatal error" not in feedback)

        self.assertNotEqual(status, 0)


if __name__ == '__main__':
    Test().test()
