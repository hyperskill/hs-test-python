import unittest
import os
from inspect import cleandoc
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestDynamicOutput(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin=[self.in1, self.in2])
        ]

    def in1(self, out):
        if out != '1\n2\n':
            0/0
        return '3\n4'

    def in2(self, out):
        if out != '5\n6\n':
            0/0
        return '7\n8\n'

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult.correct()


class Test(unittest.TestCase):
    def test(self):
        file = __file__.replace(os.sep, '.')[:-3]
        file = file[file.find('.tests.') + 1: file.rfind('.') + 1] + 'main'
        status, feedback = TestDynamicOutput(file).run_tests()

        self.assertEqual('test OK', feedback)
        self.assertEqual(status, 0)
