import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestOutOfInput2(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin=[lambda x: '1',
                            lambda x: '2',
                            lambda x: '3',
                            (2, lambda x: '4')])
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult.correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestOutOfInput2(
            'tests.outcomes.test_out_of_input_2.program'
        ).run_tests()

        self.assertTrue("Exception in test #1" in feedback)
        self.assertTrue(
            "Probably your program run out of input " +
            "(tried to read more than expected)" in feedback)

        self.assertTrue('EOFError: EOF when reading a line' in feedback)

        self.assertTrue("Fatal error" not in feedback)

        self.assertNotEqual(status, 0)
