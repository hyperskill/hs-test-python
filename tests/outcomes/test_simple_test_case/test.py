import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase, SimpleTestCase


class TesSimpleTestCase(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            SimpleTestCase(stdin="123", stdout="123\n123", feedback=''),
            SimpleTestCase(stdin="567", stdout="567\n567", feedback='')
        ]


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TesSimpleTestCase(
            'tests.outcomes.test_simple_test_case.program'
        ).run_tests()

        self.assertEqual('test OK', feedback)
        self.assertEqual(status, 0)
