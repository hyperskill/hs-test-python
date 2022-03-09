import unittest

from hstest.check_result import CheckResult
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.exception.outcomes import ErrorWithFeedback
from hstest.stage_test import StageTest


class TestRunTestInsideTest(StageTest):

    @dynamic_test
    def test(self):
        status, feedback = TestRunTestInsideTest().run_tests()
        if status != 0:
            raise ErrorWithFeedback(feedback)
        return CheckResult.correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestRunTestInsideTest().run_tests()

        self.assertEqual(status, -1)
        self.assertTrue('Error in test #1'
                        '\n\nError during testing\n\nCannot start the testing process more than once' in feedback)


if __name__ == '__main__':
    Test().test()
