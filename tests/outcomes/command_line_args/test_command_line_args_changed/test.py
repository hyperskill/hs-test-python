import unittest

from hstest.check_result import wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest
from hstest.testing.tested_program import TestedProgram


class TestCommandLineArgsChanged(StageTest):
    @dynamic_test
    def test(self):
        main = TestedProgram('main')
        main.start("123", "234", "345")
        return wrong("")


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestCommandLineArgsChanged().run_tests()
        self.assertNotEqual(status, 0)

        self.assertEqual(
            feedback,
            "Wrong answer in test #1\n" +
            "\n" +
            "Arguments: 123 234 345"
        )


if __name__ == '__main__':
    Test().test()
