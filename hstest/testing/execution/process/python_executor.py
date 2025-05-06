from __future__ import annotations

from hstest.testing.execution.process_executor import ProcessExecutor
from hstest.testing.execution.searcher.python_searcher import PythonSearcher


class PythonExecutor(ProcessExecutor):
    def __init__(self, source_name: str | None = None) -> None:
        super().__init__(PythonSearcher().find(source_name))

    def _execution_command(self, *args: str) -> list[str]:
        return ["python", "-u", self.runnable.file, *list(args)]
