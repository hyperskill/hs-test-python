import os
import re
from typing import Callable, Optional, Tuple

from hstest.common.file_utils import walk_user_files
from hstest.exception.outcomes import ErrorWithFeedback
from hstest.testing.execution.runnable_file import RunnableFile, file_contents_cached


class JavascriptRunnableFile(RunnableFile):
    main_searcher = re.compile(r'(^|\n) *function +main +\( *\)', re.M)

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

            files = [f for f in files if f.endswith('.js') and file_filter(folder, f)]

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
                        contents[file] = file_content
                        file_contents_cached[path] = contents[file]

            has_main = {f: False for f in files}

            for file in files:
                source = contents[file]

                if JavascriptRunnableFile.main_searcher.search(source) is not None:
                    has_main[file] = True

            candidates = [f for f in files if has_main[f]]

            if len(candidates) == 1:
                return folder, candidates[0]

            if len(candidates) > 1:
                str_files = ', '.join(f'"{f}"' for f in candidates)
                raise ErrorWithFeedback(
                    f'Cannot decide which file to run out of the following: {str_files}\n'
                    'They all have "function main()". Leave one file with main function.')

            if len(candidates) == 0:
                str_files = ', '.join(f'"{f}"' for f in candidates)
                raise ErrorWithFeedback(
                    f'Cannot decide which file to run out of the following: {str_files}\n'
                    'Please write "function main()" in one of them to indicate an entry point.')

        raise ErrorWithFeedback(
            'Cannot find a file to run.\n'
            f'Are your project files located at \"{curr_folder}\"?')

    @staticmethod
    def find(source: Optional[str]) -> 'JavascriptRunnableFile':
        if source is None:
            return JavascriptRunnableFile.find_by_nothing()
        else:
            return JavascriptRunnableFile.find_by_source_name(source)

    @staticmethod
    def find_by_source_name(source: str) -> 'JavascriptRunnableFile':
        path_to_test = source.replace('.', os.sep) + '.js'
        if not os.path.exists(path_to_test):
            return JavascriptRunnableFile.find_by_nothing()

        path, sep, module = source.rpartition('.')
        module_abs_path = os.path.abspath(path.replace('.', os.sep))
        return JavascriptRunnableFile.find_by_module(module_abs_path, module)

    @staticmethod
    def find_by_module(module_abs_path: str, module_name: str) -> 'JavascriptRunnableFile':
        module_to_test = module_name
        file_to_test = module_name + '.js'
        folder_to_test = module_abs_path
        return JavascriptRunnableFile(module_to_test, file_to_test, folder_to_test)

    @staticmethod
    def find_by_nothing() -> 'JavascriptRunnableFile':
        folder, file = JavascriptRunnableFile.runnable_searcher()
        without_py = file[:-3]
        return JavascriptRunnableFile.find_by_module(os.path.abspath(folder), without_py)
