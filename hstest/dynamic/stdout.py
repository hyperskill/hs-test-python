import io
from typing import List


class OutputMock:
    """
    original stream is used to actually see
    the test in the console and nothing else

    cloned stream is used to collect all output
    from the test and redirect to check function

    partial stream is used to collect output between
    input calls in StdinMock

    dynamic stream contains not only output
    but also injected input from the test
    """

    def __init__(self, real_out: io.TextIOWrapper):
        self.original: io.TextIOWrapper = real_out
        self.cloned: List[str] = []
        self.partial: List[str] = []
        self.dynamic: List[str] = []

    def write(self, text):
        self.original.write(text)
        self.cloned.append(text)
        self.partial.append(text)
        self.dynamic.append(text)

    def flush(self):
        self.original.flush()

    def close(self):
        self.original.close()

    def inject_input(self, user_input: str):
        self.original.write(user_input)
        self.dynamic.append(user_input)

    def reset(self):
        self.cloned = []
        self.partial = []
        self.dynamic = []
