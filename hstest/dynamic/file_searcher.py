import os
import re
from typing import Callable, Tuple

from hstest.exception.outcomes import ErrorWithFeedback

_contents_cached = {}


def runnable_searcher(abs_path_to_search: str = None,
                      file_filter: Callable[[str, str], bool] = lambda folder, file: True) -> Tuple[str, str]:
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

        files = [f for f in files if f.endswith('.py') and file_filter(folder, f)]

        if len(files) == 0:
            continue

        if len(files) == 1:
            return folder, files[0]

        contents = {}

        for file in files:
            path = os.path.abspath(os.path.join(folder, file))
            if path in _contents_cached:
                contents[file] = _contents_cached[path]
            elif os.path.exists(path):
                with open(path) as f:
                    file_content = f.read()
                    contents[file] = [
                        file_content,
                        re.compile(rf'(^|\n)import +[\w., ]*\b{file[:-3]}\b[\w., ]*', re.M),
                        re.compile(rf'(^|\n)from +\.? *\b{file[:-3]}\b +import +', re.M)
                    ]
                    _contents_cached[path] = contents[file]

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
