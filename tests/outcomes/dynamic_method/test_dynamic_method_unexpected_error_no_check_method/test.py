import unittest

from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest
from hstest.testing.tested_program import TestedProgram


class TestDynamicMethodUnexpectedErrorNoCheckMethod(StageTest):
    @dynamic_test
    def test(self):
        main = TestedProgram('main')
        main.start()
        main.execute('main')
        main.execute("main2")
        return None


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestDynamicMethodUnexpectedErrorNoCheckMethod().run_tests()
        self.assertNotEqual(status, 0)
        self.assertIn(
            "Unexpected error in test #1",
            feedback
        )
        self.assertIn(
            "UnexpectedError: Can't check result: override \"check\" method",
            feedback
        )


if __name__ == '__main__':
    Test().test()
