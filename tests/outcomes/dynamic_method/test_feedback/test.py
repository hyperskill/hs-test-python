import unittest

from hstest.check_result import CheckResult
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest


class TestFeedback(StageTest):
    @dynamic_test(feedback="feedback 1")
    def test(self):
        return CheckResult.wrong("feedback 2")


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestFeedback().run_tests()
        self.assertNotEqual(status, 0)
        self.assertEquals(
            "Wrong answer in test #1\n" +
            "\n" +
            "feedback 2\n" +
            "\n" +
            "feedback 1",
            feedback
        )


if __name__ == '__main__':
    Test().test()
