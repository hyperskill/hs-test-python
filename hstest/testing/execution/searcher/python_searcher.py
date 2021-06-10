import os
import re
from typing import Callable, Optional, Tuple

from hstest.common.file_utils import walk_user_files
from hstest.exception.outcomes import ErrorWithFeedback
from hstest.testing.execution.runnable_file import RunnableFile, file_contents_cached


class PythonRunnableFile(RunnableFile):
    def __init__(self, module: str, file: str, folder: str):
        super().__init__(file, folder)
        self.module = module

    @staticmethod
    def runnable_searcher(abs_path_to_search: str = None,
                          file_filter: Callable[[str, str], bool] = lambda folder, file: True) \
            -> Tuple[str, str]:
        if abs_path_to_search is None:
            abs_path_to_search = os.getcwd()

        curr_folder = os.path.abspath(abs_path_to_search)

        for folder, dirs, files in walk_user_files(curr_folder):

            files = [f for f in files if f.endswith('.py') and file_filter(folder, f)]

            if len(files) == 0:
                continue

            if len(files) == 1:
                return folder, files[0]

            contents = {}

            for file in files:
                path = os.path.abspath(os.path.join(folder, file))
                if path in file_contents_cached:
                    contents[file] = file_contents_cached[path]
                elif os.path.exists(path):
                    with open(path) as f:
                        file_content = f.read()
                        contents[file] = [
                            file_content,
                            re.compile(rf'(^|\n)import +[\w., ]*\b{file[:-3]}\b[\w., ]*', re.M),
                            re.compile(rf'(^|\n)from +\.? *\b{file[:-3]}\b +import +', re.M)
                        ]
                        file_contents_cached[path] = contents[file]

            is_imported = {f: False for f in files}
            has_name_main = {f: False for f in files}

            for file in files:
                source = contents[file][0]
                if '__name__' in source and '__main__' in source:
                    has_name_main[file] = True

                for f, (s, r1, r2) in contents.items():
                    if r1.search(source) is not None or r2.search(source) is not None:
                        is_imported[f] = True

            candidates_by_import = [f for f in files if not is_imported[f]]

            if len(candidates_by_import) == 1:
                return folder, candidates_by_import[0]

            candidates_by_name_main = [f for f in files if has_name_main[f]]

            if len(candidates_by_name_main) == 1:
                return folder, candidates_by_name_main[0]

            candidates_import_main = [f for f in candidates_by_import if has_name_main[f]]

            if len(candidates_import_main) == 1:
                return folder, candidates_import_main[0]

            if len(candidates_import_main) > 1:
                str_files = ', '.join(f'"{f}"' for f in candidates_import_main)
                raise ErrorWithFeedback(
                    f'Cannot decide which file to run out of the following: {str_files}\n'
                    'They all have "if __name__ == \'__main__\'". Leave one file with this line.')

            str_files = ', '.join(
                f'"{f}"' for f in (candidates_by_import if len(candidates_by_import) else files))

            raise ErrorWithFeedback(
                f'Cannot decide which file to run out of the following: {str_files}\n'
                'Write "if __name__ == \'__main__\'" in one of them to mark it as an entry point.')

        raise ErrorWithFeedback(
            'Cannot find a file to import and run your code.\n'
            f'Are your project files located at \"{curr_folder}\"?')

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
        return PythonRunnableFile(module_to_test, file_to_test, folder_to_test)

    @staticmethod
    def find_by_nothing() -> 'PythonRunnableFile':
        folder, file = PythonRunnableFile.runnable_searcher()
        without_py = file[:-3]
        return PythonRunnableFile.find_by_module(os.path.abspath(folder), without_py)
