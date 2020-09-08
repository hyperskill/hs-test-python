import unittest
import os
from inspect import cleandoc
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestCustomChecker(StageTest):
    def generate(self) -> List[TestCase]:
        return [
            TestCase(
                attach='4\n-in\n123\nout\n234\n',
                args=['-in', '123', 'out', '234'],
                check_function=self.custom_check
            ),
        ]

    def custom_check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == attach, '')


class Test(unittest.TestCase):
    def test(self):
        file = __file__.replace(os.sep, '.')[:-3]
        file = file[file.find('.tests.') + 1: file.rfind('.') + 1] + 'main'
        status, feedback = TestCustomChecker(file).run_tests()

        self.assertEqual('test OK', feedback)
        self.assertEqual(status, 0)
