import unittest

from hstest.check_result import correct, wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest


class TestRepeatingWithParametrizedTests(StageTest):

    data = [
        1, 2, 3, 4, 5, 6
    ]

    @dynamic_test(repeat=5, data=data)
    def test(self, x):
        return correct()

    @dynamic_test()
    def test2(self):
        return wrong('')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestRepeatingWithParametrizedTests(source_name='main').run_tests()
        self.assertNotEqual(status, 0)
        self.assertEqual("Wrong answer in test #31", feedback)


if __name__ == '__main__':
    Test().test()
