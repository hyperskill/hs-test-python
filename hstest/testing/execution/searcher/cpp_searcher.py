import re

from hstest.testing.execution.filtering.main_filter import MainFilter
from hstest.testing.execution.runnable.runnable_file import RunnableFile
from hstest.testing.execution.searcher.base_searcher import BaseSearcher


class CppSearcher(BaseSearcher):

    @property
    def extension(self) -> str:
        return '.cpp'

    def search(self, where: str = None) -> RunnableFile:
        main_func_searcher = re.compile(r'(^|\n)\s*int\s+main\s*\(\s*\)', re.M)

        return self._search(
            where,
            force_content_filters=[
                MainFilter(
                    'int main()',
                    source=lambda s: main_func_searcher.search(s) is not None
                ),
            ]
        )
