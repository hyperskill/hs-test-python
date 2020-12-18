import unittest
from typing import List

from hstest.check_result import wrong
from hstest.stage_test import StageTest
from hstest.test_case import TestCase
from hstest.testing.tested_program import TestedProgram


class TestCommandLineArgumentsFailedDynamicTesting3(StageTest):
    def test1(self):
        pr = TestedProgram('main')
        pr.start("-in", "123", "-out", "234")

        pr2 = TestedProgram('main2')
        pr2.start("--second", "main")

        return wrong('')

    def generate(self) -> List[TestCase]:
        return [
            TestCase(dynamic_testing=self.test1)
        ]


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestCommandLineArgumentsFailedDynamicTesting3('main').run_tests()
        self.assertNotEqual(status, 0)

        self.assertEqual(
            feedback,
            "Wrong answer in test #1\n" +
            "\n" +
            "Please find below the output of your program during this failed test.\n" +
            "\n" +
            "---\n" +
            "\n" +
            "Arguments for main.py: -in 123 -out 234\n" +
            "Arguments for main2.py: --second main\n" +
            "\n" +
            "4\n" +
            "-in\n" +
            "123\n" +
            "-out\n" +
            "234"
        )


if __name__ == '__main__':
    Test().test()
