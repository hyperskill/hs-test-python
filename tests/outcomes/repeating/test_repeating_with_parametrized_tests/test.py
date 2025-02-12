from hstest.check_result import correct, wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestRepeatingWithParametrizedTests(UserErrorTest):
    contain = "Wrong answer in test #31"

    data = [1, 2, 3, 4, 5, 6]

    @dynamic_test(repeat=5, data=data)
    def test(self, x):
        return correct()

    @dynamic_test()
    def test2(self):
        return wrong("")
