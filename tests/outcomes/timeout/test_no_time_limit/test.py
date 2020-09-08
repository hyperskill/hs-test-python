import unittest
import os
from inspect import cleandoc
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestNoTimeLimit(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(time_limit=-1),
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult.correct()


@unittest.skip
class Test(unittest.TestCase):
    def test(self):
        file = __file__.replace(os.sep, '.')[:-3]
        file = file[file.find('.tests.') + 1: file.rfind('.') + 1] + 'main'
        status, feedback = TestNoTimeLimit(file).run_tests()

        self.assertTrue('test OK', feedback)
        self.assertEqual(status, 0)
