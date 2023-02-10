import re

from hstest.testing.execution.filtering.main_filter import MainFilter
from hstest.testing.execution.runnable.runnable_file import RunnableFile
from hstest.testing.execution.searcher.base_searcher import BaseSearcher


class GoSearcher(BaseSearcher):

    @property
    def extension(self) -> str:
        return '.go'

    def search(self, where: str = None) -> RunnableFile:
        package_searcher = re.compile(r'package main', re.M)
        main_func_searcher = re.compile(r'(^|\n) *func +main *\( *\)', re.M)

        return self._search(
            where,
            force_content_filters=[
                MainFilter(
                    'package main',
                    source=lambda s: package_searcher.search(s) is not None
                ),
                MainFilter(
                    'func main()',
                    source=lambda s: main_func_searcher.search(s) is not None
                ),
            ]
        )
