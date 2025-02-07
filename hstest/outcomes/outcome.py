from __future__ import annotations

from hstest.common.reflection_utils import str_to_stacktrace
from hstest.common.utils import clean_text
from hstest.dynamic.output.output_handler import OutputHandler
from hstest.exception.outcomes import (
    CompilationError,
    ErrorWithFeedback,
    ExceptionWithFeedback,
    WrongAnswer,
)
from hstest.exception.testing import FileDeletionError, InfiniteLoopException, TimeLimitException


class Outcome:
    def __init__(
        self, test_number: int = 0, error_text: str = "", stack_trace: str = ""
    ) -> None:
        self.test_number: int = test_number
        self.error_text: str = error_text
        self.stack_trace: str = stack_trace

    def get_type(self) -> str:
        raise NotImplementedError

    def __str__(self) -> str:
        if self.test_number == 0:
            when_error_happened = " during testing"
        elif self.test_number > 0:
            when_error_happened = f" in test #{self.test_number}"
        else:
            when_error_happened = ""

        result = self.get_type() + when_error_happened

        if self.error_text:
            result += "\n\n" + clean_text(self.error_text.strip())

        if self.stack_trace:
            result += "\n\n" + clean_text(self.stack_trace.strip())

        full_out = OutputHandler.get_dynamic_output()
        full_err = str_to_stacktrace(OutputHandler.get_err())
        arguments = self.__get_args()

        trimmed_out = self.__trim_lines(full_out)
        trimmed_err = self.__trim_lines(full_err)

        worth_showing_err = (
            len(full_err.strip()) != 0 and full_err.strip() not in result
        )
        worth_showing_out = (
            len(full_out.strip()) != 0 and full_out.strip() not in result
        )
        worth_showing_args = len(arguments.strip()) != 0

        from hstest.stage_test import StageTest

        test_run = StageTest.curr_test_run

        if worth_showing_out or worth_showing_err or worth_showing_args:
            result += "\n\n"
            if worth_showing_out or worth_showing_err:
                result += "Please find below the output of your program during this failed test.\n"
                if test_run and test_run.input_used:
                    result += "Note that the '>' character indicates the beginning of the input line.\n"
                result += "\n---\n\n"

            if worth_showing_args:
                result += arguments + "\n\n"

            if worth_showing_out:
                if worth_showing_err:
                    result += "stdout:\n"
                result += trimmed_out + "\n\n"

            if worth_showing_err:
                result += "stderr:\n" + trimmed_err

        return result.strip()

    @staticmethod
    def __get_args():
        arguments = ""

        from hstest.stage_test import StageTest

        test_run = StageTest.curr_test_run

        if test_run is not None:
            tested_programs = test_run.tested_programs
            programs_with_args = [p for p in tested_programs if len(p.run_args)]

            for pr in programs_with_args:
                arguments += "Arguments"
                if len(tested_programs) > 1:
                    arguments += f" for {pr}"
                pr_args = [f'"{arg}"' if " " in arg else arg for arg in pr.run_args]
                arguments += f': {" ".join(pr_args)}\n'

            arguments = arguments.strip()

        return arguments

    @staticmethod
    def __trim_lines(full_out):
        result = ""

        max_lines_in_output = 250
        lines = full_out.splitlines()
        is_output_too_long = len(lines) > max_lines_in_output

        if is_output_too_long:
            result += (
                f"[last {max_lines_in_output} lines of output are shown, "
                f"{len(lines) - max_lines_in_output} skipped]\n"
            )
            last_lines = lines[-max_lines_in_output:]
            result += "\n".join(last_lines)
        else:
            result += full_out

        return result.strip()

    @staticmethod
    def get_outcome(ex: BaseException, curr_test: int):
        from hstest.outcomes.compilation_error_outcome import CompilationErrorOutcome
        from hstest.outcomes.error_outcome import ErrorOutcome
        from hstest.outcomes.exception_outcome import ExceptionOutcome
        from hstest.outcomes.unexpected_error_outcome import UnexpectedErrorOutcome
        from hstest.outcomes.wrong_answer_outcome import WrongAnswerOutcome

        if isinstance(ex, WrongAnswer):
            return WrongAnswerOutcome(curr_test, ex)

        if isinstance(ex, ExceptionWithFeedback):
            return ExceptionOutcome(curr_test, ex)

        if isinstance(ex, CompilationError):
            return CompilationErrorOutcome(ex)

        if isinstance(
            ex,
            ErrorWithFeedback
            | FileDeletionError
            | TimeLimitException
            | InfiniteLoopException
            | KeyboardInterrupt,
        ):
            return ErrorOutcome(curr_test, ex)

        return UnexpectedErrorOutcome(curr_test, ex)
