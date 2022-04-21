from hstest.check_result import wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.testing.tested_program import TestedProgram
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestCommandLineArgsChanged(UserErrorTest):
    contain = """
        Wrong answer in test #1

        Arguments: 123 234 345
        """

    @dynamic_test
    def test(self):
        main = TestedProgram('main')
        main.start("123", "234", "345")
        return wrong("")
