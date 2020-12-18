import unittest

from hstest.check_result import wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest
from hstest.testing.tested_program import TestedProgram


class TestDynamicMethodProgramNotFinishedAfterTestButExceptionHappened(StageTest):
    @dynamic_test
    def test(self):
        pr = TestedProgram('main')

        out1 = pr.start()
        if out1 != "Server started!\n":
            return wrong("")

        return None


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestDynamicMethodProgramNotFinishedAfterTestButExceptionHappened().run_tests()
        self.assertNotEqual(status, 0)
        self.assertEqual(
            feedback,
            "Exception in test #1\n" +
            "\n" +
            "Probably your program run out of input (tried to read more than expected)\n" +
            "\n" +
            "Traceback (most recent call last):\n" +
            "  File \"main.py\", line 2, in <module>\n" +
            "    print(\"S1: \" + input())\n" +
            "EOFError: EOF when reading a line\n" +
            "\n" +
            "Please find below the output of your program during this failed test.\n" +
            "\n" +
            "---\n" +
            "\n" +
            "Server started!"
        )


if __name__ == '__main__':
    Test().test()
