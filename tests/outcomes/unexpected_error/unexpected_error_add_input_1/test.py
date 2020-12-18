import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class UnexpectedErrorAddInput1(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin=[lambda x: f'{0/0}'])
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = UnexpectedErrorAddInput1('main').run_tests()

        self.assertEqual(status, -1)
        self.assertTrue('Unexpected error in test #1'
                        '\n\nWe have recorded this bug and will fix it soon.' in feedback)

        self.assertTrue('ZeroDivisionError: division by zero' in feedback)
