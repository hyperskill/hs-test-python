import unittest

from hstest.check_result import correct
from hstest.common.reflection_utils import get_main
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest
from hstest.testing.tested_program import TestedProgram


class InfiniteLoopTestLine11(StageTest):
    @dynamic_test
    def test(self):
        main = TestedProgram(get_main())
        main.start()
        return correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = InfiniteLoopTestLine11().run_tests(debug=True)
        self.assertIn(
            "Error in test #1\n" +
            "\n" +
            "Infinite loop detected.\n" +
            "No input request for the last 500 lines being printed.",
            feedback)
        self.assertNotEqual(status, 0)


if __name__ == '__main__':
    Test().test()
