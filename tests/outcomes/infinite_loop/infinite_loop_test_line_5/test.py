import unittest

from hstest.check_result import correct
from hstest.common.reflection_utils import get_main
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest
from hstest.testing.tested_program import TestedProgram


class InfiniteLoopTestLine5(StageTest):
    @dynamic_test
    def test(self):
        main = TestedProgram(get_main())
        main.start()
        return correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = InfiniteLoopTestLine5().run_tests(debug=True)
        self.assertIn(
            "Error in test #1\n" +
            "\n" +
            "Infinite loop detected.\n" +
            "Last 100 lines your program printed have 20 blocks of 5 lines of the same text.",
            feedback)
        self.assertNotEqual(status, 0)


if __name__ == '__main__':
    Test().test()
