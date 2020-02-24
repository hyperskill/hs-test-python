import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestOpenFileAndNotClose(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(files={'in.txt': '123'})
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestOpenFileAndNotClose(
            'tests.outcomes.test_open_file_and_not_close.program'
        ).run_tests()

        self.assertEqual('test OK', feedback)
        self.assertEqual(status, 0)
