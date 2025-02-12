from hstest import CheckResult, StageTest, TestedProgram, dynamic_test


class UnexpectedErrorAddInput1(StageTest):

    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start()

        output = program.execute("test")
        if output != "test\n":
            return CheckResult.wrong("")

        output = program.execute("test\n")
        if output != "test\n":
            return CheckResult.wrong("")

        output = program.execute("test\n\n")
        if output != "test\nempty\n":
            return CheckResult.wrong("")

        output = program.execute("test\n\n\n")
        if output != "test\nempty\nempty\n":
            return CheckResult.wrong("")

        output = program.execute("\ntest\n\n\n")
        if output != "empty\ntest\nempty\nempty\n":
            return CheckResult.wrong("")

        output = program.execute("test\n\ntest\n\ntest\n\n\n")
        if output != "test\nempty\ntest\nempty\ntest\nempty\nempty\n":
            return CheckResult.wrong("")

        return CheckResult.correct()
