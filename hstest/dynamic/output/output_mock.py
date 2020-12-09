import io
from typing import List

from hstest.dynamic.output.infinite_loop_detector import loop_detector
from hstest.testing.execution_options import ignore_stdout


class OutputMock:
    """
    original stream is used to actually see
    the test in the console and nothing else

    cloned stream is used to collect all output
    from the test and redirect to check function

    partial stream is used to collect output between
    input calls in InputMock

    dynamic stream contains not only output
    but also injected input from the test
    """

    def __init__(self, real_out: io.TextIOWrapper):
        class RealOutputMock:
            def __init__(self, out: io.TextIOWrapper):
                self.out = out

            def write(self, text):
                if not ignore_stdout:
                    self.out.write(text)

            def flush(self):
                self.out.flush()

            def close(self):
                self.out.close()

        self._original: RealOutputMock = RealOutputMock(real_out)
        self._cloned: List[str] = []
        self._partial: List[str] = []
        self._dynamic: List[str] = []

    @property
    def original(self):
        return self._original

    @property
    def cloned(self) -> str:
        return ''.join(self._cloned)

    @property
    def dynamic(self) -> str:
        return ''.join(self._dynamic)

    @property
    def partial(self) -> str:
        result = ''.join(self._partial)
        self._partial = []
        return result

    def write(self, text):
        self._original.write(text)
        self._cloned.append(text)
        self._dynamic.append(text)
        self._partial.append(text)
        loop_detector.write(text)

    def flush(self):
        self._original.flush()

    def close(self):
        self._original.close()

    def inject_input(self, user_input: str):
        self._original.write(user_input)
        self._dynamic.append(user_input)

    def reset(self):
        self._cloned = []
        self._partial = []
        self._dynamic = []
        loop_detector.reset()
