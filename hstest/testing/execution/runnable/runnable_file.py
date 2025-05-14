from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hstest.testing.execution.filtering.file_filter import File, Folder


class RunnableFile:
    def __init__(self, folder: Folder, file: File) -> None:
        self.folder = folder
        self.file = file

    def path(self) -> Path:
        return Path(self.folder) / self.file
