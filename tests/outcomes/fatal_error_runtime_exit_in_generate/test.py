import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class FatalErrorRuntimeExitInGenerate(StageTest):

    def generate(self) -> List[TestCase]:
        import os
        os.__dict__['_exit'](0)
        return [
            TestCase()
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = FatalErrorRuntimeExitInGenerate(
            'tests.outcomes.fatal_error_runtime_exit_in_generate.program'
        ).run_tests()

        self.assertIn('Fatal error during testing, please '
                      'send the report to support@hyperskill.org', feedback)

        self.assertIn('ExitException', feedback)
        self.assertEqual(status, -1)
