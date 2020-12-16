import unittest

from hstest.check_result import wrong
from hstest.common.reflection_utils import get_main
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest
from hstest.testing.tested_program import TestedProgram


class TestCommandLineArgumentsFailedDynamicMethod2(StageTest):
    @dynamic_test
    def test1(self):
        pr = TestedProgram(get_main())
        pr.start("-in", "123", "-out", "234")
        return wrong('')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestCommandLineArgumentsFailedDynamicMethod2(get_main()).run_tests()
        self.assertNotEqual(status, 0)

        self.assertEqual(
            feedback,
            "Wrong answer in test #1\n" +
            "\n" +
            "Arguments: -in 123 -out 234"
        )


if __name__ == '__main__':
    Test().test()
