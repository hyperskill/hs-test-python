import unittest
from time import sleep

from hstest.common.reflection_utils import get_main
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest
from hstest.testing.tested_program import TestedProgram


class InfiniteLoopTestInputRequest(StageTest):
    @dynamic_test
    def test(self):
        main = TestedProgram(get_main())
        main.start()
        main.stop_input()
        sleep(0.005)
        return None


class Test(unittest.TestCase):
    def test(self):
        status, feedback = InfiniteLoopTestInputRequest().run_tests()
        self.assertIn(
            "Error in test #1\n" +
            "\n" +
            "Infinite loop detected.\n" +
            "Between the last 20 input requests the texts being printed are identical.",
            feedback)
        self.assertNotEqual(status, 0)


if __name__ == '__main__':
    Test().test()
