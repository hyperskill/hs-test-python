from __future__ import annotations

import re
from typing import TYPE_CHECKING

from hstest.testing.execution.filtering.main_filter import MainFilter
from hstest.testing.execution.searcher.base_searcher import BaseSearcher

if TYPE_CHECKING:
    from hstest.testing.execution.runnable.runnable_file import RunnableFile


class CppSearcher(BaseSearcher):
    @property
    def extension(self) -> str:
        return ".cpp"

    def search(self, where: str | None = None) -> RunnableFile:
        main_func_searcher = re.compile(r"(^|\n)\s*int\s+main\s*\(.*\)", re.MULTILINE)

        return self._search(
            where,
            force_content_filters=[
                MainFilter("int main()", source=lambda s: main_func_searcher.search(s) is not None),
            ],
        )
