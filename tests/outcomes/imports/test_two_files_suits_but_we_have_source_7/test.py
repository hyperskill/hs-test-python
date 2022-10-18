from hstest import CheckResult, dynamic_test, StageTest, TestedProgram


class TestImportRelativeError2(StageTest):
    source = 'main1'

    @dynamic_test
    def test(self):
        pr = TestedProgram()
        return CheckResult(pr.start() == 'main1\n', '')
