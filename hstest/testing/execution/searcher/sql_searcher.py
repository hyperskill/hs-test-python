from hstest.testing.execution.runnable.runnable_file import RunnableFile
from hstest.testing.execution.searcher.base_searcher import BaseSearcher


class SQLSearcher(BaseSearcher):

    @property
    def extension(self) -> str:
        return '.sql'

    def search(self, where: str = None) -> RunnableFile:
        return self._base_search(where)
