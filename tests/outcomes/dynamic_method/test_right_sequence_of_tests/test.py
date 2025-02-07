from hstest.check_result import CheckResult, wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestRightSequenceOfTests(UserErrorTest):
    contain = """
    Wrong answer in test #15

    x == 14
    """

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
        return wrong(f"x == {self.x}")
