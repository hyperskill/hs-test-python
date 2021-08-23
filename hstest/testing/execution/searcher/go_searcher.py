import os
import re
from typing import Optional

from hstest.testing.execution.runnable_file import MainFilter, RunnableFile


class GoRunnableFile(RunnableFile):

    @staticmethod
    def runnable_searcher(where_to_search: str = None) -> RunnableFile:
        main_searcher = re.compile(r'(^|\n) *func +main +\( *\)', re.M)
        return RunnableFile.search(
            '.go',
            where_to_search,
            main_filter=MainFilter(
                "func main()",
                source=lambda s: main_searcher.search(s) is not None
            )
        )

    @staticmethod
    def find(source: Optional[str]) -> 'GoRunnableFile':
        if source is None:
            return GoRunnableFile.find_by_nothing()
        else:
            return GoRunnableFile.find_by_source_name(source)

    @staticmethod
    def find_by_source_name(source: str) -> 'GoRunnableFile':
        if source.endswith('.go'):
            source = source[:-3].replace(os.sep, '.')

        path_to_test = source.replace('.', os.sep) + '.go'
        if not os.path.exists(path_to_test):
            return GoRunnableFile.find_by_nothing()

        path, sep, file = source.rpartition('.')
        folder = os.path.abspath(path.replace('.', os.sep))
        return GoRunnableFile(folder, file + '.go')

    @staticmethod
    def find_by_nothing() -> 'GoRunnableFile':
        runnable = GoRunnableFile.runnable_searcher()
        return GoRunnableFile(runnable.folder, runnable.file)
