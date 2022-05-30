from hstest import dynamic_test, CheckResult, StageTest, TestedProgram


class UnexpectedErrorAddInput1(StageTest):
    data = [
        ("\ntest", 2),
        ("\n\ntest\n", 3),
        ("test\ntest\n\n\ntest\n\n\n", 7),
        ("\n\ntest\ntest\ntest\n\n", 6)
    ]

    @dynamic_test(data=data)
    def test(self, inp, correct_lines_number):
        program = TestedProgram()
        program.start()
        output = program.execute(inp)

        if f"Input line number {correct_lines_number}" not in output or \
                f"Input line number {correct_lines_number + 1}" in output:
            return CheckResult.wrong('')

        return CheckResult.correct()
