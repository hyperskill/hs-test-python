from __future__ import annotations

from typing import Any, TYPE_CHECKING

from hstest.dynamic.output.colored_output import BLUE, RESET
from hstest.dynamic.output.infinite_loop_detector import loop_detector
from hstest.exception.outcomes import UnexpectedError
from hstest.testing.execution_options import ignore_stdout
from hstest.testing.settings import Settings

if TYPE_CHECKING:
    import io

    from hstest.dynamic.input.input_mock import Condition


class ConditionalOutput:
    def __init__(self, condition: Condition) -> None:
        self.condition = condition
        self.output: list[str] = []


class OutputMock:
    """original stream is used to actually see
    the test in the console and nothing else.

    cloned stream is used to collect all output
    from the test and redirect to check function

    partial stream is used to collect output between
    input calls in InputMock

    dynamic stream contains not only output
    but also injected input from the test
    """

    def __init__(self, real_out: io.TextIOWrapper, is_stderr: bool = False) -> None:
        class RealOutputMock:
            def __init__(self, out: io.TextIOWrapper) -> None:
                self.out = out

            def write(self, text) -> None:
                if not ignore_stdout:
                    self.out.write(text)

            def flush(self) -> None:
                self.out.flush()

            def close(self) -> None:
                self.out.close()

        self._original: RealOutputMock = RealOutputMock(real_out)
        self._cloned: list[str] = []  # used in check function
        self._dynamic: list[str] = []  # used to append inputs
        self._partial: dict[Any, ConditionalOutput] = {}  # separated outputs for each program
        self._is_stderr = is_stderr

    @property
    def original(self):
        return self._original

    @property
    def cloned(self) -> str:
        return "".join(self._cloned)

    @property
    def dynamic(self) -> str:
        return "".join(self._dynamic)

    def partial(self, obj: Any) -> str:
        output = self._partial[obj].output
        result = "".join(output)
        output.clear()
        return result

    def write(self, text) -> None:
        partial_handler = self.__get_partial_handler()

        if partial_handler is None:
            self._original.write(BLUE + text + RESET)
            return

        if not self._is_stderr or Settings.catch_stderr:
            self._original.write(text)
            self._cloned.append(text)
            self._dynamic.append(text)
            partial_handler.append(text)

        loop_detector.write(text)

    def getvalue(self) -> None:
        pass

    def flush(self) -> None:
        self._original.flush()

    def close(self) -> None:
        self._original.close()

    def inject_input(self, user_input: str) -> None:
        self._original.write(user_input)
        self._dynamic.append(user_input)

    def reset(self) -> None:
        self._cloned.clear()
        self._dynamic.clear()
        for value in self._partial.values():
            value.output.clear()
        loop_detector.reset()

    def install_output_handler(self, obj: Any, condition: Condition) -> None:
        if obj in self._partial:
            msg = "Cannot install output handler from the same program twice"
            raise UnexpectedError(msg)
        self._partial[obj] = ConditionalOutput(condition)

    def uninstall_output_handler(self, obj: Any) -> None:
        if obj not in self._partial:
            msg = "Cannot uninstall output handler that doesn't exist"
            raise UnexpectedError(msg)
        del self._partial[obj]

    def __get_partial_handler(self):
        for handler in self._partial.values():
            if handler.condition():
                return handler.output
        return None
