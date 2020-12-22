import unittest
from inspect import cleandoc

from hstest import StageTest, TestedProgram, correct, dynamic_test


class TestImportRelativeError2(StageTest):

    @dynamic_test
    def test(self):
        pr = TestedProgram()
        pr.start()
        return correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestImportRelativeError2().run_tests()

        self.assertIn(cleandoc(
            """
            Error in test #1

            Cannot decide which file to run out of the following: "main1.py", "main2.py"
            Write "if __name__ == '__main__'" in one of them to mark it as an entry point.
            """), feedback)


if __name__ == '__main__':
    Test().test()
