import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class FatalErrorGeneratingTests(StageTest):

    def generate(self) -> List[TestCase]:
        x = 0 / 0
        return [
            TestCase()
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = FatalErrorGeneratingTests(
            'tests.outcomes.fatal_error_generating_tests.program'
        ).run_tests()

        self.assertEqual(status, -1)
        self.assertTrue('Fatal error during testing, please '
                        'send the report to Hyperskill team.' in feedback)
