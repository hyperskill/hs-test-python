import re

from hstest.testing.execution.filtering.main_filter import MainFilter
from hstest.testing.execution.runnable.runnable_file import RunnableFile
from hstest.testing.execution.searcher.base_searcher import BaseSearcher


class GoSearcher(BaseSearcher):

    @property
    def extension(self) -> str:
        return '.go'

    def search(self, where_to_search: str = None) -> RunnableFile:
        main_searcher = re.compile(r'(^|\n) *func +main +\( *\)', re.M)
        return self._search(
            where_to_search,
            main_filter=MainFilter(
                "func main()",
                source=lambda s: main_searcher.search(s) is not None
            )
        )
