import unittest

from hstest.check_result import wrong
from hstest.common.reflection_utils import get_main
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest
from hstest.testing.tested_program import TestedProgram


class TestCommandLineArgsChanged(StageTest):
    @dynamic_test
    def test(self):
        main = TestedProgram(get_main())
        main.start("123", "234", "345")
        return wrong("")


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestCommandLineArgsChanged(get_main()).run_tests()
        self.assertNotEqual(status, 0)

        self.assertEqual(
            feedback,
            "Wrong answer in test #1\n" +
            "\n" +
            "Arguments: 123 234 345"
        )


if __name__ == '__main__':
    Test().test()
