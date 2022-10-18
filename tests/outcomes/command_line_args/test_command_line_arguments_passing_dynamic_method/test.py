from hstest.check_result import CheckResult
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest
from hstest.testing.tested_program import TestedProgram


class TestCommandLineArgumentsPassingDynamicMethod(StageTest):
    @dynamic_test
    def test1(self):
        pr = TestedProgram('main')
        out = pr.start("-in", "123", "-out", "234")
        return CheckResult(out == "4\n-in\n123\n-out\n234\n", '')

    @dynamic_test
    def test2(self):
        pr = TestedProgram('main')
        out = pr.start("-in", "435", "-out", "567", "789")
        return CheckResult(out == "5\n-in\n435\n-out\n567\n789\n", '')
