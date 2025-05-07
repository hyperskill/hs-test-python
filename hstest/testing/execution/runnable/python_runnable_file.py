from __future__ import annotations

from hstest.testing.execution.runnable.runnable_file import RunnableFile


class PythonRunnableFile(RunnableFile):
    def __init__(self, folder: str, file: str, module: str) -> None:
        super().__init__(folder, file)
        self.module = module
