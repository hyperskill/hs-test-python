from hstest.testing.execution.runnable.runnable_file import RunnableFile
from hstest.testing.execution.searcher.base_searcher import BaseSearcher


class GoSearcher(BaseSearcher):

    @property
    def extension(self) -> str:
        return '.go'

    def search(self, where: str = None) -> RunnableFile:
        return self._simple_search(where, "func main()", r'(^|\n) *func +main +\( *\)')
