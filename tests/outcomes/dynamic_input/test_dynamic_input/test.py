import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestDynamicInput(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin=["1234", self.in1, self.in2],
                     attach="12340000\n23451111\n34562222\n"),
            TestCase(stdin=["4321", self.in3, self.in4],
                     attach="43210000\n54321111\n65432222\n")
        ]

    def in1(self, out):
        if out != "12340000\n":
            0/0
        return '2345'

    def in2(self, out):
        if out != "23451111\n":
            0/0
        return "3456"

    def in3(self, out):
        if out != "43210000\n":
            0/0
        return "5432"

    def in4(self, out):
        if out != "54321111\n":
            0/0
        return "6543"

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == attach, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestDynamicInput(source_name='main').run_tests()
        self.assertEqual('test OK', feedback)
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
