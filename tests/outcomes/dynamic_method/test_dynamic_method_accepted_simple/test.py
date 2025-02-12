from hstest.check_result import correct, wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest
from hstest.testing.tested_program import TestedProgram


class TestDynamicMethodAcceptedSimple(StageTest):
    @dynamic_test
    def test(self):
        pr = TestedProgram("main")

        out1 = pr.start()
        if out1 != "Program started!\n":
            return wrong("")

        out3 = pr.execute("input1")
        if out3 != "S1: input1\n":
            return wrong("")

        out5 = pr.execute("input2")
        if out5 != "S2: input2\n":
            return wrong("")

        return correct()
