import unittest
import os
from inspect import cleandoc
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class UnexpectedErrorRuntimeExitInDynamicInput(StageTest):

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
        file = __file__.replace(os.sep, '.')[:-3]
        file = file[file.find('.tests.') + 1: file.rfind('.') + 1] + 'main'
        status, feedback = UnexpectedErrorRuntimeExitInDynamicInput(file).run_tests()

        self.assertIn('Unexpected error in test #3'
                      '\n\nWe have recorded this bug and will fix it soon.', feedback)

        self.assertIn('ExitException', feedback)
        self.assertEqual(status, -1)
