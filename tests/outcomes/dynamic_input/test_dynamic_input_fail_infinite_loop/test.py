import unittest
from typing import List

from hstest.check_result import wrong
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestDynamicInputFailInfiniteLoop(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin=[lambda x: wrong("Wrong")])
        ]


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestDynamicInputFailInfiniteLoop().run_tests()
        self.assertNotEqual(status, 0)
        self.assertEqual(
            feedback,
            "Wrong answer in test #1\n" +
            "\n" +
            "Wrong"
        )


if __name__ == '__main__':
    Test().test()
