from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from hstest.testing.execution.filtering.file_filter import File


class RunnableFile:
    def __init__(self, folder: Path, file: File) -> None:
        self.folder = folder
        self.file = file

    def path(self) -> Path:
        return self.folder / self.file
