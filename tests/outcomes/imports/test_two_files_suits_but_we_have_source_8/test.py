from hstest import CheckResult, StageTest, TestedProgram, dynamic_test


class TestImportRelativeError2(StageTest):
    source = 'main2'

    @dynamic_test
    def test(self):
        pr = TestedProgram()
        return CheckResult(pr.start() == 'main2\n', '')
