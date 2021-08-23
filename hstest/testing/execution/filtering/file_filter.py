import re
from typing import Callable, Dict

Folder = str
File = str
Source = str
Sources = Dict[File, Source]
Filter = Callable[[Folder, File, Source], bool]

no_filter: Filter = lambda *a, **kw: True


class FileFilter:
    def __init__(self,
                 init_files: Callable[[Folder, Sources], None] = no_filter,
                 folder: Callable[[Folder], bool] = no_filter,
                 file: Callable[[File], bool] = no_filter,
                 source: Callable[[Source], bool] = no_filter,
                 generic: Filter = no_filter):
        self.init_files = init_files
        self.folder = folder
        self.file = file
        self.source = source
        self.generic = generic
        self.filtered = set()

    @staticmethod
    def regex_filter(regex: str):
        return lambda s: re.compile(regex, re.M).search(s) is not None

    def init_filter(self, folder: Folder, sources: Sources):
        self.init_files(folder, sources)

    def filter(self, folder: Folder, file: File, source: Source) -> bool:
        return self.folder(folder) \
            and self.file(file) \
            and self.source(source) \
            and self.generic(folder, file, source)
