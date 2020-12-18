import unittest

from hstest.check_result import correct
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest
from hstest.testing.tested_program import TestedProgram


class TestCommandLineArgsChanged(StageTest):
    @dynamic_test
    def test(self):
        main = TestedProgram()
        main.start()
        return correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestCommandLineArgsChanged().run_tests()
        self.assertEqual(status, 0)
        self.assertEqual(feedback, "test OK")


if __name__ == '__main__':
    Test().test()
