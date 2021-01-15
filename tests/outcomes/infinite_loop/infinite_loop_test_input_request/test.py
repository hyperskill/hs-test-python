import unittest
from time import sleep

from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest
from hstest.testing.tested_program import TestedProgram


class InfiniteLoopTestInputRequest(StageTest):
    @dynamic_test
    def test(self):
        main = TestedProgram('main')
        main.start()
        main.stop_input()
        sleep(0.005)
        return None


class Test(unittest.TestCase):
    def test(self):
        status, feedback = InfiniteLoopTestInputRequest().run_tests()
        self.assertEqual(
            "Error in test #1\n" +
            "\n" +
            "Program run out of input. You tried to read more, than expected.\n" +
            "\n" +
            "Please find below the output of your program during this failed test.\n" +
            "\n" +
            "---\n" +
            "\n" +
            "Long Line Long Line Long Line",
            feedback)
        self.assertNotEqual(status, 0)


if __name__ == '__main__':
    Test().test()
