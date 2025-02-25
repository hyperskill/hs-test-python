from __future__ import annotations

from typing import TYPE_CHECKING

from hstest.testing.execution.searcher.base_searcher import BaseSearcher

if TYPE_CHECKING:
    from hstest.testing.execution.runnable.runnable_file import RunnableFile


class JavascriptSearcher(BaseSearcher):
    @property
    def extension(self) -> str:
        return ".js"

    def search(self, where: str | None = None) -> RunnableFile:
        return self._simple_search(where, "function main()", r"(^|\n) *function +main +\( *\)")
