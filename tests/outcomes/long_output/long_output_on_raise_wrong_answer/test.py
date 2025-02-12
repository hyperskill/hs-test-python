from hstest import TestedProgram, WrongAnswer, dynamic_test
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestWrongOutputWithTooLongOutput(UserErrorTest):
    contain = [f"A {i} line" for i in range(350, 600)]
    not_contain = [f"A {i} line" for i in range(0, 350)]

    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start()
        raise WrongAnswer("")
