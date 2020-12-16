import unittest

from hstest.check_result import correct, wrong
from hstest.common.reflection_utils import get_main
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest
from hstest.testing.tested_program import TestedProgram


class TestDontReturnOutputAfterExecution(StageTest):
    @dynamic_test
    def test(self):
        main = TestedProgram(get_main())
        main.set_return_output_after_execution(False)

        out = main.start()
        if len(out) != 0:
            return wrong("Output should be empty")

        out = main.get_output()
        if out != "Initial text\n":
            return wrong("Output is wrong")

        for i in range(2):
            if len(main.execute('')) != 0:
                return wrong("Output should be empty")

        out = main.get_output()
        if out != "1 to 2\n2 to 3\n":
            return wrong("Output is wrong")

        main.set_return_output_after_execution(True)

        if main.execute("") != "3 to 4\n":
            return wrong("Output should not be empty")

        if len(main.get_output()) != 0:
            return wrong(
                "get_output() should return an empty string at the end")

        return correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestDontReturnOutputAfterExecution().run_tests(debug=True)
        self.assertEqual('test OK', feedback)
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
