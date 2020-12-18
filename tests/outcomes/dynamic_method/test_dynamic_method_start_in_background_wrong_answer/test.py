import unittest
from time import sleep

from hstest.check_result import wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest
from hstest.testing.tested_program import TestedProgram


class TestDynamicMethodStartInBackgroundWrongAnswer(StageTest):
    @dynamic_test
    def test(self):
        server = TestedProgram('main')

        server.start_in_background()
        sleep(0.15)
        return wrong('')


@unittest.skip('Background execution in python doesn\'t work')
class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestDynamicMethodStartInBackgroundWrongAnswer().run_tests()
        self.assertNotEqual(status, 0)
        self.assertEqual(
            feedback,
            "Wrong answer in test #1\n" +
            "\n" +
            "Please find below the output of your program during this failed test.\n" +
            "\n" +
            "---\n" +
            "\n" +
            "Server started!\n" +
            "S1"
        )


if __name__ == '__main__':
    Test().test()
