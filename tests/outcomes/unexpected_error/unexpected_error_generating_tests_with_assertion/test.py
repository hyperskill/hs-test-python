import unittest
from typing import Any

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest


class UnexpectedErrorGeneratingTestsWithAssertion(StageTest):

    def generate(self):
        assert False

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = UnexpectedErrorGeneratingTestsWithAssertion(source_name='main').run_tests()

        self.assertEqual(status, -1)
        self.assertTrue('Unexpected error during testing'
                        '\n\nWe have recorded this bug and will fix it soon.' in feedback)
