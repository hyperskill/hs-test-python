import unittest
from typing import List

from hstest.check_result import wrong
from hstest.stage_test import StageTest
from hstest.test_case import TestCase
from hstest.testing.tested_program import TestedProgram


class TestCommandLineArgumentsFailedDynamicTesting4(StageTest):
    def test1(self):
        pr = TestedProgram('main')
        pr.start()

        pr2 = TestedProgram('main2')
        pr2.start("--second", "main")

        return wrong('')

    def generate(self) -> List[TestCase]:
        return [
            TestCase(dynamic_testing=self.test1)
        ]


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestCommandLineArgumentsFailedDynamicTesting4(source_name='main').run_tests()
        self.assertNotEqual(status, 0)

        self.assertEqual(
            feedback,
            "Wrong answer in test #1\n" +
            "\n" +
            "Please find below the output of your program during this failed test.\n" +
            "\n" +
            "---\n" +
            "\n" +
            "Arguments for main2.py: --second main\n" +
            "\n" +
            "0"
        )


if __name__ == '__main__':
    Test().test()
