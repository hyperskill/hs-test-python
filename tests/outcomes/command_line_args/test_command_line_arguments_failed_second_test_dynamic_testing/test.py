import unittest
from typing import List

from hstest.check_result import CheckResult
from hstest.common.reflection_utils import get_main
from hstest.stage_test import StageTest
from hstest.test_case import TestCase
from hstest.testing.tested_program import TestedProgram


class TestCommandLineArgumentsFailedSecondTestDynamicTesting(StageTest):
    def test1(self):
        pr = TestedProgram(get_main())
        pr.start("-in", "123", "-out", "234")
        return CheckResult(False, '')

    def test2(self):
        pr2 = TestedProgram(get_main('main2'))
        pr2.start("--second", "main")
        return CheckResult(True, '')

    def generate(self) -> List[TestCase]:
        return [
            TestCase(dynamic_testing=self.test2),
            TestCase(dynamic_testing=self.test1)
        ]


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestCommandLineArgumentsFailedSecondTestDynamicTesting(get_main()).run_tests()
        self.assertNotEqual(status, 0)

        self.assertEqual(
            feedback,
            "Wrong answer in test #2\n" +
            "\n" +
            "Please find below the output of your program during this failed test.\n" +
            "\n" +
            "---\n" +
            "\n" +
            "Arguments: -in 123 -out 234\n" +
            "\n" +
            "4\n" +
            "-in\n" +
            "123\n" +
            "-out\n" +
            "234"
        )


if __name__ == '__main__':
    Test().test()
