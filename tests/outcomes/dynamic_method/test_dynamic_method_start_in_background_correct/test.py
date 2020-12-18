import unittest
from time import sleep

from hstest.check_result import correct, wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest
from hstest.testing.tested_program import TestedProgram


class TestDynamicMethodStartInBackgroundCorrect(StageTest):
    @dynamic_test
    def test(self):
        server = TestedProgram('main')

        server.start_in_background()
        sleep(0.05)

        out = server.get_output()
        if out != "Server started!\n":
            return wrong("")

        sleep(0.1)

        out = server.get_output()
        if out != "S1\n":
            return wrong("")

        sleep(0.2)

        out = server.get_output()
        if out != "S2\nS3\n":
            return wrong("")

        return correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestDynamicMethodStartInBackgroundCorrect().run_tests()
        self.assertEqual(status, 0)
        self.assertEqual(
            feedback,
            "test OK"
        )


if __name__ == '__main__':
    Test().test()
