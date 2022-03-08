import unittest

from hstest.check_result import CheckResult
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest


class TestParametrizedData3(StageTest):

    test_data = [
        [1], [2], [3], [4], [5]
    ]

    counter = 0

    @dynamic_test(data=test_data)
    def test(self, a):
        self.counter += 1
        print(a)
        return CheckResult(self.counter == a, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestParametrizedData3(source_name='main').run_tests()
        self.assertEqual(status, 0)
        self.assertEqual('test OK', feedback)


if __name__ == '__main__':
    Test().test()
