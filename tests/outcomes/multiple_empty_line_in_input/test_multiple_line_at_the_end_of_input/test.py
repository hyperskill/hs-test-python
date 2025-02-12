from hstest import CheckResult, StageTest, TestedProgram, dynamic_test


class UnexpectedErrorAddInput1(StageTest):
    data = [
        ("test", 1),
        ("test\n", 1),
        ("test\n\n", 2),
        ("test\n\n\n", 3),
        ("test\n\n\n\n", 4),
    ]

    @dynamic_test(data=data)
    def test(self, inp, correct_lines_number):
        program = TestedProgram()
        program.start()
        output = program.execute(inp)

        if (
            f"Input line number {correct_lines_number}" not in output
            or f"Input line number {correct_lines_number + 1}" in output
        ):
            return CheckResult.wrong("")

        return CheckResult.correct()
