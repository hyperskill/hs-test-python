import unittest

from hstest import CheckResult, StageTest, TestedProgram, dynamic_test


class TestImportRelativeError2(StageTest):
    @dynamic_test
    def test(self):
        pr = TestedProgram('main1')
        return CheckResult(pr.start() == 'main1\n', '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestImportRelativeError2().run_tests()
        self.assertEqual('test OK', feedback)


if __name__ == '__main__':
    Test().test()
