from hstest.check_result import CheckResult
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.testing.tested_program import TestedProgram
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestCommandLineArgumentsFailedSecondTestDynamicMethod(UserErrorTest):
    contain = """
    Wrong answer in test #2

    Arguments: --second main
    """

    @dynamic_test
    def test1(self):
        pr = TestedProgram("main")
        pr.start("-in", "123", "-out", "234")
        return CheckResult(True, "")

    @dynamic_test
    def test2(self):
        pr2 = TestedProgram("main2")
        pr2.start("--second", "main")
        return CheckResult(False, "")
