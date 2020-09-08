import unittest
from typing import Any

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest


class FatalErrorNotGeneratingTests(StageTest):

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = FatalErrorNotGeneratingTests(
            'tests.outcomes.fatal_error_not_generating_tests.program'
        ).run_tests()

        self.assertEqual(status, -1)
        self.assertTrue('Unexpected error during testing'
                        '\n\nWe have recorded this bug and will fix it soon.' in feedback)

        self.assertTrue('Can\'t create tests: override "generate" method' in feedback)
