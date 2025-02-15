from __future__ import annotations

import sys

from hstest.testing.execution.process_executor import ProcessExecutor
from hstest.testing.execution.searcher.python_searcher import PythonSearcher


class PythonExecutor(ProcessExecutor):
    def __init__(self, source_name: str | None = None) -> None:
        super().__init__(PythonSearcher().find(source_name))

    def _execution_command(self, *args: str):
        cmd = ["python"]
        if sys.platform == "win32":
            # Set UTF-8 encoding for stdin/stdout on Windows
            cmd.extend(["-X", "utf8"])
        cmd.extend(["-u", self.runnable.file, *list(args)])
        return cmd
