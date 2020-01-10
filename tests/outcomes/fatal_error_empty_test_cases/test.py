import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class FatalErrorEmptyTestCases(StageTest):

    def generate(self) -> List[TestCase]:
        return []

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = FatalErrorEmptyTestCases(
            'tests.outcomes.fatal_error_empty_test_cases.program'
        ).run_tests()

        self.assertEqual(status, -1)
        self.assertTrue('Fatal error during testing, please '
                        'send the report to support@hyperskill.org' in feedback)

        self.assertTrue('No tests provided by "generate" method' in feedback)
