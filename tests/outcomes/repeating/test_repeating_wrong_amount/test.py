import unittest

from hstest.check_result import correct
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest


class TestRepeatingWrongAmount(StageTest):

    @dynamic_test(repeat=-1)
    def test(self, x):
        return correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestRepeatingWrongAmount('main').run_tests()
        self.assertNotEqual(status, 0)
        self.assertIn("UnexpectedError: Dynamic test \"test\" should not "
                      "be repeated < 0 times, found -1", feedback)


if __name__ == '__main__':
    Test().test()
