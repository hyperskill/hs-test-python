from hstest.check_result import correct, wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestRepeating3(UserErrorTest):
    contain = "Wrong answer in test #11"

    @dynamic_test(repeat=5)
    def test(self):
        return correct()

    @dynamic_test(repeat=5)
    def test3(self):
        return correct()

    @dynamic_test()
    def test2(self):
        return wrong('')
