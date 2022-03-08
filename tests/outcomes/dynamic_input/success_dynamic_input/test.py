import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class SuccessDynamicInput(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin=[lambda x: x],
                     attach="Hello\nHello\n"),

            TestCase(stdin=[lambda x: 'Hi'],
                     attach="Hello\nHi\n"),

            TestCase(stdin=[lambda x: 'Hihi1',
                            lambda x: 'Hihi2'],
                     attach="Hello\nHihi1\n"),

            TestCase(stdin=[lambda x: '', lambda x: 'Hihi3'],
                     attach="Hello\n\n"),

            TestCase(stdin=[lambda x: '1', lambda x: 'Hey'],
                     attach="Hello\nHey\n"),

            TestCase(stdin=[lambda x: '2', lambda x: 'Hey'],
                     attach="Hello\n2\n"),

            TestCase(stdin=[lambda x: 'Hi before', lambda x: 'Hi after'],
                     attach="Hello\nHi before\n"),

            TestCase(stdin=[lambda x: "řĦπ"],
                     attach="Hello\nřĦπ\n")
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == attach, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = SuccessDynamicInput(source_name='main').run_tests()
        self.assertEqual(status, 0)
        self.assertEqual(feedback, 'test OK')


if __name__ == '__main__':
    Test().test()
