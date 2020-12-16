import unittest

from hstest.check_result import CheckResult
from hstest.common.reflection_utils import get_main
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest


class TestWrongData2(StageTest):

    test_data = []

    counter = 0

    @dynamic_test(data=test_data)
    def test(self, a):
        self.counter += 1
        print(a)
        return CheckResult(self.counter == len(a), '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestWrongData2(get_main()).run_tests()
        self.assertNotEqual(status, 0)
        self.assertIn('UnexpectedError: Data passed to dynamic method "test" '
                      'should not be empty.', feedback)


if __name__ == '__main__':
    Test().test()
