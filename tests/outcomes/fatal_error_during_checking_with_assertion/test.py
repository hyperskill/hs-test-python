import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class FatalErrorDuringCheckingWithAssertion(StageTest):

    def generate(self) -> List[TestCase]:
        return [TestCase()]

    def check(self, reply: str, attach: Any) -> CheckResult:
        if reply == 'Hello World\n':
            assert False
        return CheckResult(True, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = FatalErrorDuringCheckingWithAssertion(
            'tests.outcomes.fatal_error_during'
            '_checking_with_assertion.program'
        ).run_tests()

        self.assertEqual(status, -1)
        self.assertTrue('Fatal error in test #1, please '
                        'send the report to support@hyperskill.org' in feedback)
