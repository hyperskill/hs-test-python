import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class UnexpectedErrorGeneratingTests(StageTest):

    def generate(self) -> List[TestCase]:
        x = 0 / 0
        return [
            TestCase()
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = UnexpectedErrorGeneratingTests('main').run_tests()

        self.assertEqual(status, -1)
        self.assertTrue('Unexpected error during testing'
                        '\n\nWe have recorded this bug and will fix it soon.' in feedback)
