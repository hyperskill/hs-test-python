import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class FatalErrorDuringChecking(StageTest):

    def generate(self) -> List[TestCase]:
        return [TestCase()]

    def check(self, reply: str, attach: Any) -> CheckResult:
        x = 0 / 0
        return CheckResult(True, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = FatalErrorDuringChecking(
            'tests.outcomes.fatal_error_during_checking.program'
        ).run_tests()

        self.assertEqual(status, -1)
        self.assertTrue('Fatal error in test #1, please '
                        'send the report to Hyperskill team.' in feedback)
