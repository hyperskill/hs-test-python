from hstest import TestedProgram, correct, dynamic_test
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestImportRelativeError2(UserErrorTest):
    contain = """
            Error in test #1

            Cannot decide which file to run out of the following: "main1.py", "main2.py"
            Write "if __name__ == '__main__'" in one of them to mark it as an entry point.
            """

    @dynamic_test
    def test(self):
        pr = TestedProgram()
        pr.start()
        return correct()
