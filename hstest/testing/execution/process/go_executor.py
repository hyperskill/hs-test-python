from __future__ import annotations

from pathlib import Path

from hstest.common.os_utils import is_windows
from hstest.testing.execution.process_executor import ProcessExecutor
from hstest.testing.execution.searcher.go_searcher import GoSearcher


class GoExecutor(ProcessExecutor):
    def __init__(self, source_name: str | None = None) -> None:
        super().__init__(GoSearcher().find(source_name))

        self.without_go = self.runnable.file[: -len(GoSearcher().extension)]

        if is_windows():
            self.executable = self.without_go
            self.file_name = Path(self.executable + ".exe")
        else:
            self.executable = f"./{self.without_go}"
            self.file_name = Path(self.without_go)

    def _compilation_command(self) -> list[str]:
        return ["go", "build", self.runnable.file]

    def _filter_compilation_error(self, error: str) -> str:
        error_lines = [line for line in error.splitlines() if not line.startswith("#")]
        return "\n".join(error_lines)

    def _execution_command(self, *args: str) -> list[str]:
        return [self.executable, *list(args)]

    def _cleanup(self) -> None:
        self.file_name.unlink(missing_ok=True)
