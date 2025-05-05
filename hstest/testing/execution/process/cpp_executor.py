from __future__ import annotations

import os
from pathlib import Path

from hstest.common.os_utils import is_windows
from hstest.testing.execution.process_executor import ProcessExecutor
from hstest.testing.execution.searcher.cpp_searcher import CppSearcher


class CppExecutor(ProcessExecutor):
    def __init__(self, source_name: str | None = None) -> None:
        super().__init__(CppSearcher().find(source_name))

        self.without_extension = os.path.splitext(self.runnable.file)[0]  # noqa: PTH122

        if is_windows():
            self.executable = self.without_extension
            self.file_name = Path(self.executable + ".exe")
        else:
            self.executable = f'./{self.without_extension}'
            self.file_name = self.without_extension

    def _compilation_command(self):
        return ['g++', '-std=c++20', '-pipe', '-O2', '-static', '-o', self.file_name, self.runnable.file]

    def _filter_compilation_error(self, error: str) -> str:
        return error

    def _execution_command(self, *args: str) -> list[str]:
        return [self.executable, *list(args)]

    def _cleanup(self) -> None:
        self.file_name.unlink(missing_ok=True)
