from hstest.testing.execution.runnable.runnable_file import RunnableFile
from hstest.testing.execution.searcher.base_searcher import BaseSearcher


class ShellSearcher(BaseSearcher):

    @property
    def extension(self) -> str:
        return '.sh'

    def search(self, where: str = None) -> RunnableFile:
        return self._simple_search(where, "# main", r'(^|\n)# *main')
