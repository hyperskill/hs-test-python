from hstest.check_result import wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.testing.tested_program import TestedProgram
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestCommandLineArgumentsFailedDynamicMethod2(UserErrorTest):
    contain = """
    Wrong answer in test #1

    Arguments: -in 123 -out 234
    """

    @dynamic_test
    def test1(self):
        pr = TestedProgram('main')
        pr.start("-in", "123", "-out", "234")
        return wrong('')
