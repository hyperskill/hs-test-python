from hstest import dynamic_test, wrong, TestedProgram
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestWrongOutputWithTooLongOutput(UserErrorTest):
    contain = [f'A {i} line' for i in range(1, 250)] + ['[last 250 lines of output are shown, 1 skipped]']
    not_contain = [f'A {i} line' for i in range(0, 1)]

    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start()
        return wrong('')
