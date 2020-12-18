import unittest

from hstest.check_result import correct
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest
from hstest.testing.tested_program import TestedProgram


class InfiniteLoopTestLine1(StageTest):
    @dynamic_test
    def test(self):
        main = TestedProgram('main')
        main.start()
        return correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = InfiniteLoopTestLine1().run_tests()
        self.assertIn(
            "Error in test #1\n" +
            "\n" +
            "Infinite loop detected.\n" +
            "Last 100 lines your program printed are the same.",
            feedback)
        self.assertNotEqual(status, 0)


if __name__ == '__main__':
    Test().test()
