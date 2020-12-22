import unittest

from hstest import CheckResult, StageTest, TestedProgram, dynamic_test


class TestImportRelativeError2(StageTest):
    source = 'main2'

    @dynamic_test
    def test(self):
        pr = TestedProgram()
        return CheckResult(pr.start() == 'main2\n', '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestImportRelativeError2().run_tests()
        self.assertEqual('test OK', feedback)


if __name__ == '__main__':
    Test().test()
