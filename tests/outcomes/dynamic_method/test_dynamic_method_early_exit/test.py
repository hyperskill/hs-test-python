import unittest

from hstest.check_result import correct, wrong
from hstest.common.reflection_utils import get_main
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest
from hstest.testing.tested_program import TestedProgram


class TestDynamicMethodEarlyExit(StageTest):
    @dynamic_test
    def test(self):
        pr = TestedProgram(get_main())

        out1 = pr.start()
        if out1 != "Server started!\n":
            return wrong("")

        out1 = pr.execute("main")
        if out1 != "S1: main\n":
            return wrong("")

        pr.execute("main2")
        return correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestDynamicMethodEarlyExit().run_tests()
        self.assertNotEqual(status, 0)
        self.assertEqual(
            feedback,
            "Error in test #1\n" +
            "\n" +
            "The program main.py has unexpectedly terminated.\n" +
            "It finished execution too early, should continue running.\n" +
            "\n" +
            "Please find below the output of your program during this failed test.\n" +
            "Note that the '>' character indicates the beginning of the input line.\n" +
            "\n" +
            "---\n" +
            "\n" +
            "Server started!\n" +
            "> main\n" +
            "S1: main"
        )


if __name__ == '__main__':
    Test().test()
