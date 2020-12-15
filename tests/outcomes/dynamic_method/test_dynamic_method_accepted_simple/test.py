import unittest

from hstest.common.reflection_utils import get_main
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest


class TestDynamicMethodAcceptedSimple(StageTest):
    @dynamic_test
    def test(self):
        pass


class Test(unittest.TestCase):
    def test(self):
        return
        status, feedback = TestDynamicMethodAcceptedSimple(get_main()).run_tests()

        self.assertEqual('test OK', feedback)
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
