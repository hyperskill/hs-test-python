from hstest import dynamic_test, TestedProgram, wrong
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestWrongOutputWithTooLongOutput(UserErrorTest):
    contain = [f'A {i} line' for i in range(1, 250)]
    not_contain = '[last 250 lines of output are shown, 1 skipped]'

    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start()
        return wrong('')
