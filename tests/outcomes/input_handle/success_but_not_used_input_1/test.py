import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.common.reflection_utils import get_main
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class SuccessButNotUsedInput1(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin='1\nnotnum\n', attach='1\n'),
            TestCase(stdin='2\nnotnum\n', attach='2\nnotnum\n'),
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == attach, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = SuccessButNotUsedInput1(get_main()).run_tests()
        self.assertEqual(status, 0)
        self.assertEqual(feedback, 'test OK')
