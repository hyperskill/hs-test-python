import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class UnexpectedErrorRuntimeExitInGenerate(StageTest):

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
        status, feedback = UnexpectedErrorRuntimeExitInGenerate('main').run_tests()

        self.assertIn('Unexpected error during testing'
                      '\n\nWe have recorded this bug and will fix it soon.', feedback)

        self.assertIn('ExitException', feedback)
        self.assertEqual(status, -1)
