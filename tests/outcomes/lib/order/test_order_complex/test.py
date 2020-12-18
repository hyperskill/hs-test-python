import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestOrderComplex(StageTest):

    x = 0

    @dynamic_test(order=5)
    def test4(self):
        self.x += 1
        return CheckResult(self.x == 8, 'test3')

    @dynamic_test(order=-5)
    def test0(self):
        self.x += 1
        return CheckResult(self.x == 4, 'test0')

    @dynamic_test(order=-1)
    def test1(self):
        self.x += 1
        return CheckResult(self.x == 5, 'test1')

    @dynamic_test()
    def test2(self):
        self.x += 1
        return CheckResult(self.x == 6, 'test2')

    @dynamic_test
    def test3(self):
        self.x += 1
        return CheckResult(self.x == 7, 'test3')

    def generate(self) -> List[TestCase]:
        return [
            TestCase(),
            TestCase(check_function=self.test5),
            TestCase(dynamic_testing=self.test6),
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        self.x += 1
        return CheckResult(self.x == 1, 'test4')

    def test5(self, reply: str, attach: Any) -> CheckResult:
        self.x += 1
        return CheckResult(self.x == 2, 'test4')

    def test6(self):
        self.x += 1
        return CheckResult(self.x == 3, 'test5')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestOrderComplex('main').run_tests()
        self.assertEqual('test OK', feedback)


if __name__ == '__main__':
    Test().test()
