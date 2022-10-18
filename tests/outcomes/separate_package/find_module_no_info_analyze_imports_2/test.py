from hstest.check_result import CheckResult
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest
from hstest.testing.tested_program import TestedProgram


class FindModuleNoInfoAnalyzeImports(StageTest):
    @dynamic_test
    def test(self):
        main = TestedProgram()
        result = main.start()
        return CheckResult(
            result ==
            'Main 3\n'
            'Main 4\n'
            'Main 2\n'
            'Module no info\n', '')
