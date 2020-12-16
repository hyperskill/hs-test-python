import unittest

from hstest.check_result import correct
from hstest.common.reflection_utils import get_main
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest
from hstest.testing.tested_program import TestedProgram


class InfiniteLoopTestChar(StageTest):
    @dynamic_test
    def test(self):
        main = TestedProgram(get_main())
        main.start()
        return correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = InfiniteLoopTestChar().run_tests(debug=True)
        self.assertIn(
            "Error in test #1\n" +
            "\n" +
            "Infinite loop detected.\n" +
            "No input request for the last 5000 characters being printed.",
            feedback)
        self.assertNotEqual(status, 0)


if __name__ == '__main__':
    Test().test()
