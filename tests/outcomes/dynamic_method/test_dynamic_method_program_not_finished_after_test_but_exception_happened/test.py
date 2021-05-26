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
            "Error in test #1\n" +
            "\n" +
            "Program ran out of input. You tried to read more than expected.\n" +
            "\n" +
            "Please find below the output of your program during this failed test.\n" +
            "\n" +
            "---\n" +
            "\n" +
            "Server started!"
        )


if __name__ == '__main__':
    Test().test()
