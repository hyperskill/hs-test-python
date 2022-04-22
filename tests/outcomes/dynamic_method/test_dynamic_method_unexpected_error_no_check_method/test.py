from hstest.dynamic.dynamic_test import dynamic_test
from hstest.testing.tested_program import TestedProgram
from hstest.testing.unittest.unexepected_error_test import UnexpectedErrorTest


class TestDynamicMethodUnexpectedErrorNoCheckMethod(UnexpectedErrorTest):
    contain = [
        "Unexpected error in test #1",
        "UnexpectedError: Can't check result: override \"check\" method"
    ]

    @dynamic_test
    def test(self):
        main = TestedProgram('main')
        main.start()
        main.execute('main')
        main.execute("main2")
        return None
