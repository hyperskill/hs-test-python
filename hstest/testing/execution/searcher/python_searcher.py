import os
import re
from typing import Optional

from hstest.testing.execution.runnable_file import FileFilter, Folder, MainFilter, RunnableFile, Sources


class PythonRunnableFile(RunnableFile):
    def __init__(self, folder: str, file: str, module: str):
        super().__init__(folder, file)
        self.module = module

    @staticmethod
    def runnable_searcher(where_to_search: str = None, file_filter: FileFilter = None) -> RunnableFile:

        is_imported = {}

        def init_regexes(folder: Folder, sources: Sources):
            import_regexes = {}

            for file, source in sources.items():
                import_regexes[file] = [
                    re.compile(rf'(^|\n)import +[\w., ]*\b{file[:-3]}\b[\w., ]*', re.M),
                    re.compile(rf'(^|\n)from +\.? *\b{file[:-3]}\b +import +', re.M)
                ]

            for f in sources.keys():
                is_imported[f] = False

            for file, source in sources.items():
                for f, (r1, r2) in import_regexes.items():
                    if r1.search(source) is not None or r2.search(source) is not None:
                        is_imported[f] = True

        return RunnableFile.search(
            '.py',
            where_to_search,
            file_filter=file_filter,

            pre_main_filter=FileFilter(
                init_files=init_regexes,
                file=lambda f: not is_imported[f]
            ),

            main_filter=MainFilter(
                "if __name__ == '__main__'",
                source=lambda s: '__name__' in s and '__main__' in s
            )
        )

    @staticmethod
    def find(source: Optional[str]) -> 'PythonRunnableFile':
        if source is None:
            return PythonRunnableFile.find_by_nothing()
        else:
            return PythonRunnableFile.find_by_source_name(source)

    @staticmethod
    def find_by_source_name(source: str) -> 'PythonRunnableFile':
        path_to_test = source.replace('.', os.sep) + '.py'
        if not os.path.exists(path_to_test):
            return PythonRunnableFile.find_by_nothing()

        path, sep, module = source.rpartition('.')
        module_abs_path = os.path.abspath(path.replace('.', os.sep))
        return PythonRunnableFile.find_by_module(module_abs_path, module)

    @staticmethod
    def find_by_module(module_abs_path: str, module_name: str) -> 'PythonRunnableFile':
        module_to_test = module_name
        file_to_test = module_name + '.py'
        folder_to_test = module_abs_path
        return PythonRunnableFile(folder_to_test, file_to_test, module_to_test)

    @staticmethod
    def find_by_nothing() -> 'PythonRunnableFile':
        runnable = PythonRunnableFile.runnable_searcher()
        folder = runnable.folder
        file = runnable.file
        without_py = file[:-3]
        return PythonRunnableFile.find_by_module(os.path.abspath(folder), without_py)
