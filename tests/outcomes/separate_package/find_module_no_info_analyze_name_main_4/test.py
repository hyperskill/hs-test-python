import unittest

from hstest.check_result import CheckResult, correct
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest
from hstest.testing.tested_program import TestedProgram


class FindModuleNoInfoAnalyzeImports(StageTest):
    @dynamic_test
    def test(self):
        main = TestedProgram()
        result = main.start()
        return CheckResult(
            result ==
            'Main 4\n'
            'Main 3\n'
            'Main 2\n', '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = FindModuleNoInfoAnalyzeImports().run_tests()
        self.assertEqual(status, 0)
        self.assertEqual(feedback, 'test OK')


if __name__ == '__main__':
    Test().test()
