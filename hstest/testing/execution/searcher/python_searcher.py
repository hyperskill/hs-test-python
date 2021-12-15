import os
import re
from typing import Optional

from hstest.dynamic.output.output_handler import OutputHandler
from hstest.testing.execution.filtering.file_filter import FileFilter, Folder, Sources
from hstest.testing.execution.filtering.main_filter import MainFilter
from hstest.testing.execution.runnable.python_runnable_file import PythonRunnableFile
from hstest.testing.execution.runnable.runnable_file import RunnableFile
from hstest.testing.execution.searcher.base_searcher import BaseSearcher


class PythonSearcher(BaseSearcher):

    @property
    def extension(self) -> str:
        return '.py'

    def search(self, where_to_search: str = None, file_filter: FileFilter = None) -> RunnableFile:
        is_imported = {}

        def init_regexes(_: Folder, sources: Sources):
            import_regexes = {}

            for file, source in sources.items():
                is_imported[file] = False
                import_regexes[file] = [
                    re.compile(rf'(^|\n)import +[\w., ]*\b{file[:-3]}\b[\w., ]*', re.M),
                    re.compile(rf'(^|\n)from +\.? *\b{file[:-3]}\b +import +', re.M)
                ]

            for file, source in sources.items():
                for f, (r1, r2) in import_regexes.items():
                    if r1.search(source) is not None or r2.search(source) is not None:
                        is_imported[f] = True

        return self._search(
            where_to_search,
            file_filter=file_filter,

            pre_main_filter=FileFilter(
                init_files=init_regexes,
                file=lambda f: not is_imported[f]
            ),

            main_filter=MainFilter(
                "if __name__ == '__main__'",
                source=lambda s: '__name__' in s and '__main__' in s
            )
        )

    def find(self, source: Optional[str]) -> PythonRunnableFile:
        OutputHandler.print(f'PythonSearcher source = {source}, cwd = {os.getcwd()}')
        runnable = super().find(source)
        OutputHandler.print(f'PythonSearcher found runnable: {runnable.folder}/{runnable.file}')
        return PythonRunnableFile(runnable.folder, runnable.file, runnable.file[:-len(self.extension)])
