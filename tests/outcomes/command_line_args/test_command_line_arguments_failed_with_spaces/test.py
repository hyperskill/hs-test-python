import unittest
from typing import List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase
from hstest.testing.tested_program import TestedProgram


class TestCommandLineArgumentsFailedWithSpaces(StageTest):
    def test(self):
        pr = TestedProgram('main')
        pr.start("-spaces", "some argument with spaces",
                 "-number", "234", "-onlySpaces", "      ")
        return CheckResult(False, "See arguments below:")

    def generate(self) -> List[TestCase]:
        return [
            TestCase(dynamic_testing=self.test)
        ]


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestCommandLineArgumentsFailedWithSpaces(source_name='main').run_tests()
        self.assertNotEqual(status, 0)

        self.assertEqual(
            feedback,
            "Wrong answer in test #1\n" +
            "\n" +
            "See arguments below:\n" +
            "\n" +
            "Please find below the output of your program during this failed test.\n" +
            "\n" +
            "---\n" +
            "\n" +
            "Arguments: -spaces \"some argument with spaces\" -number 234 -onlySpaces \"      \"\n" +
            "\n" +
            "6\n" +
            "-spaces\n" +
            "some argument with spaces\n" +
            "-number\n" +
            "234\n" +
            "-onlySpaces"
        )


if __name__ == '__main__':
    Test().test()
