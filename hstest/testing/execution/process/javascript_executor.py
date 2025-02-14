from __future__ import annotations

from hstest.testing.execution.process_executor import ProcessExecutor
from hstest.testing.execution.searcher.javascript_searcher import JavascriptSearcher


class JavascriptExecutor(ProcessExecutor):
    def __init__(self, source_name: str | None = None) -> None:
        super().__init__(JavascriptSearcher().find(source_name))

    def _execution_command(self, *args: str):
        return ["node", self.runnable.file, *list(args)]
