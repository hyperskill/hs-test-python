from __future__ import annotations

from typing import TYPE_CHECKING

from hstest.testing.execution.filtering.file_filter import (
    File,
    FileFilter,
    Filter,
    Folder,
    no_filter,
    Source,
    Sources,
)

if TYPE_CHECKING:
    from collections.abc import Callable


class MainFilter(FileFilter):
    def __init__(
        self,
        program_should_contain: str,
        init_files: Callable[[Folder, Sources], None] = no_filter,
        folder: Callable[[Folder], bool] = no_filter,
        file: Callable[[File], bool] = no_filter,
        source: Callable[[Source], bool] = no_filter,
        generic: Filter = no_filter,
    ) -> None:
        super().__init__(init_files, folder, file, source, generic)
        self.program_should_contain = program_should_contain
