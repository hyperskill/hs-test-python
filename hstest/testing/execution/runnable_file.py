import os
from typing import Dict, Set

from hstest.common.file_utils import walk_user_files
from hstest.exception.outcomes import ErrorWithFeedback, UnexpectedError
from hstest.testing.execution.filtering.file_filter import File, FileFilter, Folder, Source
from hstest.testing.execution.filtering.main_filter import MainFilter

file_contents_cached = {}
search_cached = {}


class RunnableFile:
    def __init__(self, folder: Folder, file: File):
        self.folder = folder
        self.file = file

    @staticmethod
    def _get_contents(folder, files) -> Dict[File, Source]:
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

        return contents

    @staticmethod
    def search_non_cached(
            extension: str,
            where_to_search: str,
            file_filter: FileFilter,
            pre_main_filter: FileFilter,
            main_filter: MainFilter,
            post_main_filter: FileFilter) \
            -> 'RunnableFile':

        curr_folder = os.path.abspath(where_to_search)

        for folder, dirs, files in walk_user_files(curr_folder):

            contents = RunnableFile._get_contents(folder, files)

            initial_filter = FileFilter(
                file=lambda f: f.endswith(extension),
                generic=file_filter.filter
            )

            candidates = set(files)

            for curr_filter in initial_filter, pre_main_filter, main_filter, post_main_filter:
                curr_filter.init_filter(folder, contents)

                filtered_files: Set[File] = {
                    file for file in files
                    if curr_filter.filter(folder, file, contents[file])
                }

                curr_filter.filtered = filtered_files

                if len(filtered_files) == 0:
                    if curr_filter == initial_filter:
                        break
                    else:
                        continue

                if len(filtered_files) == 1:
                    file = filtered_files.pop()
                    return RunnableFile(folder, file)

                new_candidates = candidates & filtered_files
                if len(new_candidates) != 0:
                    candidates = new_candidates

                if len(candidates) == 1:
                    file = candidates.pop()
                    return RunnableFile(folder, file)

            if len(initial_filter.filtered) == 0:
                continue

            if len(candidates) > 1 and len(main_filter.filtered) > 0:
                str_files = ', '.join(f'"{f}"' for f in sorted(candidates))
                raise ErrorWithFeedback(
                    f'Cannot decide which file to run out of the following: {str_files}\n'
                    f'They all have "{main_filter.program_should_contain}". Leave one file with this line.')

            if len(candidates) == 0:
                candidates = initial_filter.filtered

            str_files = ', '.join(f'"{f}"' for f in sorted(candidates))

            raise ErrorWithFeedback(
                f'Cannot decide which file to run out of the following: {str_files}\n'
                f'Write "{main_filter.program_should_contain}" in one of them to mark it as an entry point.')

        raise ErrorWithFeedback(
            'Cannot find a file to execute your code.\n'
            f'Are your project files located at \"{curr_folder}\"?')

    @staticmethod
    def search(
            extension: str,
            where_to_search: str = None,
            *,
            file_filter: FileFilter = None,
            pre_main_filter: FileFilter = None,
            main_filter: MainFilter = None,
            post_main_filter: FileFilter = None) \
            -> 'RunnableFile':

        if not extension.startswith('.'):
            raise UnexpectedError(f'File extension "{extension}" should start with a dot')

        if where_to_search is None:
            where_to_search = os.getcwd()

        do_caching = False
        cache_key = extension, where_to_search

        if file_filter is None:
            if cache_key in search_cached:
                return search_cached[cache_key]

            do_caching = True
            file_filter = FileFilter()

        if pre_main_filter is None:
            pre_main_filter = FileFilter()

        if main_filter is None:
            main_filter = MainFilter("")

        if post_main_filter is None:
            post_main_filter = FileFilter()

        result = RunnableFile.search_non_cached(
            extension,
            where_to_search,
            file_filter,
            pre_main_filter,
            main_filter,
            post_main_filter,
        )

        if do_caching:
            search_cached[cache_key] = result

        return result
