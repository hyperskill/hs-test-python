from __future__ import annotations

from typing import TYPE_CHECKING

from hstest.testing.execution.searcher.base_searcher import BaseSearcher

if TYPE_CHECKING:
    from hstest.testing.execution.runnable.runnable_file import RunnableFile


class SQLSearcher(BaseSearcher):
    @property
    def extension(self) -> str:
        return ".sql"

    def search(self, where: str | None = None) -> RunnableFile:
        return self._base_search(where)
