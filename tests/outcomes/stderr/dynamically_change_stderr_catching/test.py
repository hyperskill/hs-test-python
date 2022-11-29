from hstest.testing.unittest.user_error_test import UserErrorTest
from hstest.testing.settings import Settings
from hstest import dynamic_test, TestedProgram, wrong

Settings.catch_stderr = False


class TestDynamicStderrCatch(UserErrorTest):
    contain = [
        'stderr:',
        'text from stderr'
    ]

    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start()

        Settings.catch_stderr = True
        program = TestedProgram()
        program.start()

        Settings.catch_stderr = False
        program = TestedProgram()
        program.start()
        return wrong('Something is wrong!')

    def after_all_tests(self):
        Settings.catch_stderr = True
