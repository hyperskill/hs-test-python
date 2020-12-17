import unittest

from hstest.check_result import CheckResult, wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest


class TestRightSequenceOfTests(StageTest):

    x = 0

    @dynamic_test
    def test1(self):
        self.x += 1
        return CheckResult(self.x == 1, "")

    @dynamic_test
    def test2(self):
        self.x += 1
        return CheckResult(self.x == 2, "")

    @dynamic_test
    def test3(self):
        self.x += 1
        return CheckResult(self.x == 3, "")

    @dynamic_test
    def test4(self):
        self.x += 1
        return CheckResult(self.x == 4, "")

    @dynamic_test
    def test5(self):
        self.x += 1
        return CheckResult(self.x == 5, "")

    @dynamic_test
    def test6(self):
        self.x += 1
        return CheckResult(self.x == 6, "")

    @dynamic_test
    def test7(self):
        self.x += 1
        return CheckResult(self.x == 7, "")

    @dynamic_test
    def test8(self):
        self.x += 1
        return CheckResult(self.x == 8, "")

    @dynamic_test
    def test9(self):
        self.x += 1
        return CheckResult(self.x == 9, "")

    @dynamic_test
    def test10(self):
        self.x += 1
        return CheckResult(self.x == 10, "")

    @dynamic_test
    def test11(self):
        self.x += 1
        return CheckResult(self.x == 11, "")

    @dynamic_test
    def test12(self):
        self.x += 1
        return CheckResult(self.x == 12, "")

    @dynamic_test
    def test13(self):
        self.x += 1
        return CheckResult(self.x == 13, "")

    @dynamic_test
    def test14(self):
        self.x += 1
        return CheckResult(self.x == 14, "")

    @dynamic_test
    def test15(self):
        return wrong(f'x == {self.x}')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestRightSequenceOfTests().run_tests()
        self.assertNotEqual(status, 0)
        self.assertEqual(
            "Wrong answer in test #15\n" +
            "\n" +
            "x == 14",
            feedback
        )


if __name__ == '__main__':
    Test().test()
