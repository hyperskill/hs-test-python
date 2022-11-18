from hstest.testing.execution.runnable.runnable_file import RunnableFile
from hstest.testing.execution.searcher.base_searcher import BaseSearcher


class TypeScriptSearcher(BaseSearcher):

    @property
    def extension(self) -> str:
        return '.ts'

    def search(self, where: str = None) -> RunnableFile:
        return self._simple_search(where, "function main()", r'(^|\n) *function +main +\( *\)')
