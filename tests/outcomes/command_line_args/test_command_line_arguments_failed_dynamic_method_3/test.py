import unittest

from hstest.check_result import wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest
from hstest.testing.tested_program import TestedProgram


class TestCommandLineArgumentsFailedDynamicMethod3(StageTest):
    @dynamic_test
    def test1(self):
        pr = TestedProgram('main')
        pr.start("-in", "123", "-out", "234")

        pr2 = TestedProgram('main2')
        pr2.start("--second", "main")

        return wrong('')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestCommandLineArgumentsFailedDynamicMethod3().run_tests()
        self.assertNotEqual(status, 0)

        self.assertEqual(
            feedback,
            "Wrong answer in test #1\n" +
            "\n" +
            "Please find below the output of your program during this failed test.\n" +
            "\n" +
            "---\n" +
            "\n" +
            "Arguments for main.py: -in 123 -out 234\n" +
            "Arguments for main2.py: --second main\n" +
            "\n" +
            "4\n" +
            "-in\n" +
            "123\n" +
            "-out\n" +
            "234"
        )


if __name__ == '__main__':
    Test().test()
