from hstest import TestedProgram, dynamic_test, wrong
from hstest.testing.settings import Settings
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestDisableStderrCatch(UserErrorTest):
    not_contain = ["stderr:", "text from stderr"]

    @dynamic_test
    def test(self):
        Settings.catch_stderr = False
        program = TestedProgram()
        program.start()
        Settings.catch_stderr = True
        return wrong("Something is wrong!")
