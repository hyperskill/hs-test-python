import re

from hstest.testing.execution.filtering.main_filter import MainFilter
from hstest.testing.execution.runnable.runnable_file import RunnableFile
from hstest.testing.execution.searcher.base_searcher import BaseSearcher


class JavascriptSearcher(BaseSearcher):

    @property
    def extension(self) -> str:
        return '.js'

    def search(self, where_to_search: str = None) -> RunnableFile:
        main_searcher = re.compile(r'(^|\n) *function +main +\( *\)', re.M)
        return self._search(
            where_to_search,
            main_filter=MainFilter(
                "function main()",
                source=lambda s: main_searcher.search(s) is not None
            )
        )
