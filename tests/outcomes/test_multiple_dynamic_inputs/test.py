import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestMultipleDynamicInputs(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin=[lambda x: '1',
                            lambda x: '2',
                            lambda x: '3',
                            lambda x: '4',
                            lambda x: '5'],
                     attach="1\n2\n3\n4\n5\n"),

            TestCase(stdin=[lambda x: '1',
                            lambda x: '2',
                            lambda x: '3',
                            (2, lambda x: '4')],
                     attach="1\n2\n3\n4\n4\n"),

            TestCase(stdin=[lambda x: '1',
                            lambda x: '2',
                            (2, lambda x: '3'),
                            lambda x: '4'],
                     attach="1\n2\n3\n3\n4\n"),

            TestCase(stdin=[lambda x: '1',
                            (3, lambda x: '2'),
                            lambda x: '3',
                            lambda x: '4',
                            lambda x: '5'],
                     attach="1\n2\n2\n2\n3\n"),

            TestCase(stdin=[lambda x: '1',
                            (10, lambda x: '2'),
                            lambda x: '3',
                            lambda x: '4',
                            lambda x: '5'],
                     attach="1\n2\n2\n2\n2\n"),

            TestCase(stdin=[(2, lambda x: '1\n2'),
                            lambda x: '5',
                            lambda x: '6',
                            lambda x: '7',
                            lambda x: '8'],
                     attach="1\n2\n1\n2\n5\n"),

            TestCase(stdin=[(-1, lambda x: '1\n2'),
                            lambda x: '5',
                            lambda x: '6',
                            lambda x: '7',
                            lambda x: '8'],
                     attach="1\n2\n1\n2\n1\n"),
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == attach, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestMultipleDynamicInputs(
            'tests.outcomes.test_multiple_dynamic_inputs.program'
        ).run_tests()

        self.assertEqual('test OK', feedback)
        self.assertEqual(status, 0)
