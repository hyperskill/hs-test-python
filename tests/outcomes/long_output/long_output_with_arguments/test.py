from hstest import TestedProgram, dynamic_test, wrong
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestWrongOutputWithTooLongOutput(UserErrorTest):
    contain = "Arguments: -arg test\n\n[last 250 lines of output are shown, 1 skipped]"

    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start("-arg", "test")
        return wrong("")
