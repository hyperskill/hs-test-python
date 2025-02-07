from __future__ import annotations

from typing import TYPE_CHECKING

from hstest.testing.execution.searcher.base_searcher import BaseSearcher

if TYPE_CHECKING:
    from pathlib import Path

    from hstest.testing.execution.runnable.runnable_file import RunnableFile


class ShellSearcher(BaseSearcher):
    @property
    def extension(self) -> str:
        return ".sh"

    def search(self, where: Path | None = None) -> RunnableFile:
        return self._simple_search(where, "# main", r"(^|\n)# *main")
