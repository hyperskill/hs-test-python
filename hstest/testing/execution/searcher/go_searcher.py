from __future__ import annotations

import re
from typing import TYPE_CHECKING

from hstest.testing.execution.filtering.main_filter import MainFilter
from hstest.testing.execution.searcher.base_searcher import BaseSearcher

if TYPE_CHECKING:
    from hstest.testing.execution.runnable.runnable_file import RunnableFile


class GoSearcher(BaseSearcher):
    @property
    def extension(self) -> str:
        return ".go"

    def search(self, where: str | None = None) -> RunnableFile:
        package_searcher = re.compile(r"^\s*package\s*main", re.MULTILINE)
        main_func_searcher = re.compile(r"(^|\n)\s*func\s+main\s*\(\s*\)", re.MULTILINE)

        return self._search(
            where,
            force_content_filters=[
                MainFilter(
                    "package main",
                    source=lambda s: package_searcher.search(s) is not None,
                ),
                MainFilter(
                    "func main()",
                    source=lambda s: main_func_searcher.search(s) is not None,
                ),
            ],
        )
