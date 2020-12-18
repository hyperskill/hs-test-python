import unittest

from hstest.check_result import correct, wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest


class TestRepeating3(StageTest):

    @dynamic_test(repeat=5)
    def test(self):
        return correct()

    @dynamic_test(repeat=5)
    def test3(self):
        return correct()

    @dynamic_test()
    def test2(self):
        return wrong('')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestRepeating3('main').run_tests()
        self.assertNotEqual(status, 0)
        self.assertEqual("Wrong answer in test #11", feedback)


if __name__ == '__main__':
    Test().test()
