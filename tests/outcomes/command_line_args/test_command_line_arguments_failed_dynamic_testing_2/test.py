import unittest
from typing import List

from hstest.check_result import wrong
from hstest.common.reflection_utils import get_main
from hstest.stage_test import StageTest
from hstest.test_case import TestCase
from hstest.testing.tested_program import TestedProgram


class TestCommandLineArgumentsFailedDynamicTesting3(StageTest):
    def test1(self):
        pr = TestedProgram(get_main())
        pr.start("-in", "123", "-out", "234")
        return wrong('')

    def generate(self) -> List[TestCase]:
        return [
            TestCase(dynamic_testing=self.test1)
        ]


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestCommandLineArgumentsFailedDynamicTesting3(get_main()).run_tests()
        self.assertNotEqual(status, 0)

        self.assertEqual(
            feedback,
            "Wrong answer in test #1\n" +
            "\n" +
            "Arguments: -in 123 -out 234"
        )


if __name__ == '__main__':
    Test().test()
