from hstest.testing.execution.runnable.runnable_file import RunnableFile
from hstest.testing.execution.searcher.base_searcher import BaseSearcher


class JavascriptSearcher(BaseSearcher):

    @property
    def extension(self) -> str:
        return '.js'

    def search(self, where: str = None) -> RunnableFile:
        return self._simple_search(where, "function main()", r'(^|\n) *function +main +\( *\)')
