import os
import unittest

from hstest.check_result import correct, wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest


class TestFilesInDynamicTest(StageTest):
    @dynamic_test(files={'123.txt': '12345'})
    def test(self):
        if '123.txt' in os.listdir('.'):
            if open('123.txt').read() == '12345':
                return correct()

        return wrong('There should be a file named "123.txt" with content "12345"')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestFilesInDynamicTest().run_tests()
        self.assertEqual(
            "test OK",
            feedback
        )
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
