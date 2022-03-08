import unittest
from typing import List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase
from hstest.testing.tested_program import TestedProgram


class TestCommandLineArgumentsPassingDynamicMethod(StageTest):
    def test1(self):
        pr = TestedProgram('main')
        out = pr.start("-in", "123", "-out", "234")
        return CheckResult(out == "4\n-in\n123\n-out\n234\n", '')

    def test2(self):
        pr = TestedProgram('main')
        out = pr.start("-in", "435", "-out", "567", "789")
        return CheckResult(out == "5\n-in\n435\n-out\n567\n789\n", '')

    def generate(self) -> List[TestCase]:
        return [
            TestCase(dynamic_testing=self.test1),
            TestCase(dynamic_testing=self.test2),
        ]


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestCommandLineArgumentsPassingDynamicMethod(source_name='main').run_tests()
        self.assertEqual(status, 0)
        self.assertEqual(feedback, 'test OK')


if __name__ == '__main__':
    Test().test()
