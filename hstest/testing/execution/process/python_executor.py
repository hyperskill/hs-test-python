from __future__ import annotations

import os

from hstest.common.os_utils import is_windows
from hstest.testing.execution.process_executor import ProcessExecutor
from hstest.testing.execution.searcher.python_searcher import PythonSearcher


class PythonExecutor(ProcessExecutor):
    def __init__(self, source_name: str | None = None) -> None:
        super().__init__(PythonSearcher().find(source_name))
        # Set UTF-8 encoding for Python I/O on Windows
        if is_windows():
            os.environ["PYTHONIOENCODING"] = "utf8"

    def _execution_command(self, *args: str) -> list[str]:
        cmd = ["python"]
        if is_windows():  # Works on all Windows versions (32/64 bit)
            # Set UTF-8 encoding for stdin/stdout on Windows
            cmd.extend(["-X", "utf8"])
        cmd.extend(["-u", self.runnable.file, *list(args)])
        return cmd
