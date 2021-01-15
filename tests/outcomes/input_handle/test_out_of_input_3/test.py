import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestOutOfInput3(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin=[lambda x: '1',
                            (3, lambda x: '2'),
                            lambda x: '4'])
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult.correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestOutOfInput3('main').run_tests()

        self.assertIn(
            "Error in test #1\n" +
            "\n" +
            "Program run out of input. You tried to read more, than expected.\n",
            feedback)

        self.assertTrue("Fatal error" not in feedback)

        self.assertNotEqual(status, 0)


if __name__ == '__main__':
    Test().test()
