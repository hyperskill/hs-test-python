from hstest.check_result import wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.testing.tested_program import TestedProgram
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestCommandLineArgumentsFailedDynamicMethod4(UserErrorTest):
    contain = """
    Wrong answer in test #1

    Please find below the output of your program during this failed test.
    
    ---
    
    Arguments for main2.py: --second main
    
    0
    """  # noqa: W293

    @dynamic_test
    def test1(self):
        pr = TestedProgram("main")
        pr.start()

        pr2 = TestedProgram("main2")
        pr2.start("--second", "main")

        return wrong("")
