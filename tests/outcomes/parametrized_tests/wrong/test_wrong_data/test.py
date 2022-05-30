from hstest.check_result import CheckResult
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.testing.unittest.unexepected_error_test import UnexpectedErrorTest


class TestWrongData(UnexpectedErrorTest):
    contain = 'UnexpectedError: Data passed to dynamic method "test" ' \
              'should be of type "list" or "tuple",' \
              ' found <class \'int\'>.'

    test_data = 123

    counter = 0

    @dynamic_test(data=test_data)
    def test(self, a):
        self.counter += 1
        print(a)
        return CheckResult(self.counter == len(a), '')
