from hstest.check_result import CheckResult
from hstest.dynamic.dynamic_test import dynamic_test
from testing.unittest.unexepected_error_test import UnexpectedErrorTest


class TestWrongData2(UnexpectedErrorTest):
    contain = 'UnexpectedError: Data passed to dynamic method "test" should not be empty.'

    test_data = []

    counter = 0

    @dynamic_test(data=test_data)
    def test(self, a):
        self.counter += 1
        print(a)
        return CheckResult(self.counter == len(a), '')
