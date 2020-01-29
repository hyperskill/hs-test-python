import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class FatalErrorRuntimeExitInDynamicInput(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin=[lambda x: '123']),
            TestCase(stdin=[self.add_input_1]),
            TestCase(stdin=[self.add_input_2]),
        ]

    def add_input_1(self, stdin: str):
        return '123'

    def add_input_2(self, stdin: str):
        import sys
        sys.exit(0)
        return '123'

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = FatalErrorRuntimeExitInDynamicInput(
            'tests.outcomes.fatal_error_runtime_exit_in_dynamic_input.program'
        ).run_tests()

        self.assertIn('Fatal error in test #3, please '
                      'send the report to support@hyperskill.org', feedback)

        self.assertIn('ExitException', feedback)
        self.assertEqual(status, -1)
