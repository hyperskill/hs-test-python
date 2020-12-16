import unittest

from hstest.check_result import correct, wrong
from hstest.common.reflection_utils import get_main
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest
from hstest.testing.tested_program import TestedProgram


class TestDynamicMethodProgramNotFinishedAfterTest(StageTest):
    @dynamic_test
    def test(self):
        pr = TestedProgram(get_main())

        out1 = pr.start()
        if out1 != "Server started!\n":
            return wrong("")

        return correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestDynamicMethodProgramNotFinishedAfterTest().run_tests(debug=True)
        self.assertEqual(status, 0)
        self.assertEqual(
            feedback,
            "test OK"
        )


if __name__ == '__main__':
    Test().test()
