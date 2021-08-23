from typing import Callable

from hstest.testing.execution.filtering.file_filter import File, FileFilter, Filter, Folder, Source, Sources, no_filter


class MainFilter(FileFilter):
    def __init__(self,
                 program_should_contain: str,
                 init_files: Callable[[Folder, Sources], None] = no_filter,
                 folder: Callable[[Folder], bool] = no_filter,
                 file: Callable[[File], bool] = no_filter,
                 source: Callable[[Source], bool] = no_filter,
                 generic: Filter = no_filter):
        super().__init__(init_files, folder, file, source, generic)
        self.program_should_contain = program_should_contain
