import unittest
from time import sleep

from hstest.check_result import correct, wrong
from hstest.common.reflection_utils import get_main
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest
from hstest.testing.tested_program import TestedProgram


class TestGettingOutputWhileProgramInBackground(StageTest):
    @dynamic_test
    def test(self):
        main = TestedProgram(get_main())
        main.start_in_background()

        out = main.get_output()
        if out != '':
            return wrong('')

        sleep(0.15)

        out = main.get_output()
        if out != "Test\n":
            return wrong('')

        sleep(0.2)

        out = main.get_output()
        if out != "Test\nTest\n":
            return wrong('')

        main.stop()
        if not main.is_finished():
            return wrong("")

        return correct()


@unittest.skip('Background execution in python doesn\'t work')
class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestGettingOutputWhileProgramInBackground().run_tests()
        self.assertEqual(
            "test OK",
            feedback
        )
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
