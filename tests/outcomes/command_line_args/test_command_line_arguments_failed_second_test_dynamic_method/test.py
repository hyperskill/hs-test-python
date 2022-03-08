import unittest

from hstest.check_result import CheckResult
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest
from hstest.testing.tested_program import TestedProgram


class TestCommandLineArgumentsFailedSecondTestDynamicMethod(StageTest):
    @dynamic_test
    def test1(self):
        pr = TestedProgram('main')
        pr.start("-in", "123", "-out", "234")
        return CheckResult(True, '')

    @dynamic_test
    def test2(self):
        pr2 = TestedProgram('main2')
        pr2.start("--second", "main")
        return CheckResult(False, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestCommandLineArgumentsFailedSecondTestDynamicMethod(source_name='main').run_tests()
        self.assertNotEqual(status, 0)

        self.assertEqual(
            feedback,
            "Wrong answer in test #2\n" +
            "\n" +
            "Arguments: --second main"
        )


if __name__ == '__main__':
    Test().test()
