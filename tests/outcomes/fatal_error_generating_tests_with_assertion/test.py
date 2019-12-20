import unittest
from typing import Any

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest


class FatalErrorGeneratingTestsWithAssertion(StageTest):

    def generate(self):
        assert False

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = FatalErrorGeneratingTestsWithAssertion(
            'tests.outcomes.fatal_error_generating_tests_with_assertion.program'
        ).run_tests()

        self.assertEqual(status, -1)
        self.assertTrue('Fatal error during testing, please '
                        'send the report to Hyperskill team.' in feedback)
