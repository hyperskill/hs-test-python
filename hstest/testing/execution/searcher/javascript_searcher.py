import os
import re
from typing import Optional

from hstest.testing.execution.filtering.main_filter import MainFilter
from hstest.testing.execution.runnable_file import RunnableFile


class JavascriptRunnableFile(RunnableFile):

    @staticmethod
    def runnable_searcher(where_to_search: str = None) -> RunnableFile:
        main_searcher = re.compile(r'(^|\n) *function +main +\( *\)', re.M)
        return RunnableFile.search(
            '.js',
            where_to_search,
            main_filter=MainFilter(
                "function main()",
                source=lambda s: main_searcher.search(s) is not None
            )
        )

    @staticmethod
    def find(source: Optional[str]) -> 'JavascriptRunnableFile':
        if source is None:
            return JavascriptRunnableFile.find_by_nothing()
        else:
            return JavascriptRunnableFile.find_by_source_name(source)

    @staticmethod
    def find_by_source_name(source: str) -> 'JavascriptRunnableFile':
        if source.endswith('.js'):
            source = source[:-3].replace(os.sep, '.')

        path_to_test = source.replace('.', os.sep) + '.js'
        if not os.path.exists(path_to_test):
            return JavascriptRunnableFile.find_by_nothing()

        path, sep, file = source.rpartition('.')
        folder = os.path.abspath(path.replace('.', os.sep))
        return JavascriptRunnableFile(folder, file + '.js')

    @staticmethod
    def find_by_nothing() -> 'JavascriptRunnableFile':
        runnable = JavascriptRunnableFile.runnable_searcher()
        return JavascriptRunnableFile(runnable.folder, runnable.file)
