from __future__ import annotations

from hstest.testing.execution.process_executor import ProcessExecutor
from hstest.testing.execution.searcher.shell_searcher import ShellSearcher


class ShellExecutor(ProcessExecutor):
    def __init__(self, source_name: str | None = None) -> None:
        super().__init__(ShellSearcher().find(source_name))

    def _execution_command(self, *args: str):
        return ["bash", self.runnable.file, *list(args)]
