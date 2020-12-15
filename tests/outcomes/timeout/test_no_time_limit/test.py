import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.common.reflection_utils import get_main
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
        status, feedback = TestNoTimeLimit(get_main()).run_tests()
        self.assertTrue('test OK', feedback)
        self.assertEqual(status, 0)
