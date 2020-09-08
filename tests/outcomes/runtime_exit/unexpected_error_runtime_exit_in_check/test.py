import unittest
import os
from inspect import cleandoc
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class UnexpectedErrorRuntimeExitInCheck(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase()
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        quit(0)
        return CheckResult(True, '')


class Test(unittest.TestCase):
    def test(self):
        file = __file__.replace(os.sep, '.')[:-3]
        file = file[file.find('.tests.') + 1: file.rfind('.') + 1] + 'main'
        status, feedback = UnexpectedErrorRuntimeExitInCheck(file).run_tests()

        self.assertIn('Unexpected error in test #1'
                      '\n\nWe have recorded this bug and will fix it soon.', feedback)

        self.assertIn('ExitException', feedback)
        self.assertEqual(status, -1)
