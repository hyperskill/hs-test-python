import os
import re
from typing import Callable, Optional, Tuple

from hstest.exception.outcomes import ErrorWithFeedback
from hstest.testing.execution.runnable_file import RunnableFile, file_contents_cached


class GoRunnableFile(RunnableFile):
    main_searcher = re.compile(r'(^|\n) *func +main +\( *\) *{', re.M)

    def __init__(self, file: str, folder: str):
        super().__init__(file, folder)

    @staticmethod
    def runnable_searcher(abs_path_to_search: str = None,
                          file_filter: Callable[[str, str], bool] = lambda folder, file: True) \
            -> Tuple[str, str]:

        if abs_path_to_search is None:
            abs_path_to_search = os.getcwd()

        curr_folder = os.path.abspath(abs_path_to_search)
        test_folder = os.path.join(curr_folder, 'test')

        for folder, dirs, files in os.walk(curr_folder):
            if folder.startswith(test_folder):
                continue

            if folder == curr_folder:
                for file in 'test.py', 'tests.py':
                    if file in files:
                        files.remove(file)

            files = [f for f in files if f.endswith('.go') and file_filter(folder, f)]

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

                if GoRunnableFile.main_searcher.search(source) is not None:
                    has_main[file] = True

            candidates = [f for f in files if has_main[f]]

            if len(candidates) == 1:
                return folder, candidates[0]

            if len(candidates) > 1:
                str_files = ', '.join(f'"{f}"' for f in candidates)
                raise ErrorWithFeedback(
                    f'Cannot decide which file to run out of the following: {str_files}\n'
                    'They all have "func main()". Leave one file with main function.')

        raise ErrorWithFeedback(
            'Cannot find a file with main function.\n'
            f'Are your project files located at \"{curr_folder}\"?')

    @staticmethod
    def find(source: Optional[str]) -> 'GoRunnableFile':
        if source is None:
            return GoRunnableFile.find_by_nothing()
        else:
            return GoRunnableFile.find_by_source_name(source)

    @staticmethod
    def find_by_source_name(source: str) -> 'GoRunnableFile':
        if source.endswith('.go'):
            source = source[:-3].replace(os.sep, '.')

        path_to_test = source.replace('.', os.sep) + '.go'
        if not os.path.exists(path_to_test):
            return GoRunnableFile.find_by_nothing()

        path, sep, module = source.rpartition('.')
        folder = os.path.abspath(path.replace('.', os.sep))
        return GoRunnableFile(module + '.go', folder)

    @staticmethod
    def find_by_nothing() -> 'GoRunnableFile':
        folder, file = GoRunnableFile.runnable_searcher()
        return GoRunnableFile(file, os.path.abspath(folder))
