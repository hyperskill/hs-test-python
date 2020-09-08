import unittest
import os
from inspect import cleandoc
from typing import Any

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest


class UnexpectedErrorNotGeneratingTests(StageTest):

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, '')


class Test(unittest.TestCase):
    def test(self):
        file = __file__.replace(os.sep, '.')[:-3]
        file = file[file.find('.tests.') + 1: file.rfind('.') + 1] + 'main'
        status, feedback = UnexpectedErrorNotGeneratingTests(file).run_tests()

        self.assertEqual(status, -1)
        self.assertTrue('Unexpected error during testing'
                        '\n\nWe have recorded this bug and will fix it soon.' in feedback)

        self.assertTrue('Can\'t create tests: override "generate" method' in feedback)
