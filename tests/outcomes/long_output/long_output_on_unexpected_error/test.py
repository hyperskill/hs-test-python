from hstest import dynamic_test, TestedProgram, wrong
from hstest.testing.unittest.unexepected_error_test import UnexpectedErrorTest


class TestWrongOutputWithTooLongOutput(UnexpectedErrorTest):
    contain = [f'A {i} line' for i in range(350, 600)]
    not_contain = [f'A {i} line' for i in range(0, 350)]

    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start()
        a = 2 / 0  # noqa: F841
        return wrong('')
