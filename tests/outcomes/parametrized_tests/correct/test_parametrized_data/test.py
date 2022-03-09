import unittest

from hstest.check_result import CheckResult
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest


class TestParametrizedData(StageTest):

    test_data = [
        [1, 2],
        [2, 3],
        [3, 4],
        [4, 5],
        [5, 6]
    ]

    counter = 0

    @dynamic_test(data=test_data)
    def test(self, a, b):
        self.counter += 1
        print(a, b)
        return CheckResult(self.counter == a and self.counter + 1 == b, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestParametrizedData().run_tests()
        self.assertEqual(status, 0)
        self.assertEqual('test OK', feedback)


if __name__ == '__main__':
    Test().test()
