from hstest.check_result import correct, wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest
from hstest.testing.tested_program import TestedProgram


class TestDynamicMethodProgramNotFinishedAfterTest(StageTest):
    @dynamic_test
    def test(self):
        pr = TestedProgram("main")

        out1 = pr.start()
        if out1 != "Server started!\n":
            return wrong("")

        return correct()
