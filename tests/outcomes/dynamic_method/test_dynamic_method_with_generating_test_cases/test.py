import unittest
from typing import List

from hstest.check_result import correct
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestDynamicMethodUnexpectedErrorNoCheckMethod(StageTest):

    @dynamic_test
    def test(self):
        return correct()

    def generate(self) -> List[TestCase]:
        return [
            TestCase(dynamic_testing=lambda: correct())
        ]


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestDynamicMethodUnexpectedErrorNoCheckMethod().run_tests(debug=True)
        self.assertEqual(status, 0)
        self.assertEqual(
            "test OK",
            feedback
        )


if __name__ == '__main__':
    Test().test()
