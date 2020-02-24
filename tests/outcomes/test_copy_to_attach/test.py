import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestCopyToAttach(StageTest):

    def generate(self) -> List[TestCase]:
        tests = [
            TestCase(stdin='1234', copy_to_attach=True),
            TestCase(stdin='4321', copy_to_attach=True)
        ]
        return tests

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == attach, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestCopyToAttach(
            'tests.outcomes.test_copy_to_attach.program'
        ).run_tests()

        self.assertEqual("test OK", feedback)
        self.assertEqual(status, 0)
