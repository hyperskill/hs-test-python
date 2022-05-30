from hstest.check_result import correct
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest
from hstest.testing.tested_program import TestedProgram


class FindModuleNoInfo(StageTest):
    @dynamic_test
    def test(self):
        main = TestedProgram()
        main.start()
        return correct()
