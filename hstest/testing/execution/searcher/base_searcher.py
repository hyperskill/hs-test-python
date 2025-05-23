from __future__ import annotations

import os
import re

from hstest.common.file_utils import walk_user_files
from hstest.exception.outcomes import ErrorWithFeedback, UnexpectedError
from hstest.testing.execution.filtering.file_filter import File, FileFilter, Folder, Module, Source
from hstest.testing.execution.filtering.main_filter import MainFilter
from hstest.testing.execution.runnable.runnable_file import RunnableFile

file_contents_cached = {}
search_cached = {}


class BaseSearcher:
    @property
    def extension(self) -> str:
        msg = 'Property "extension" should be implemented'
        raise NotImplementedError(msg)

    def search(self, where_to_search: str | None = None) -> RunnableFile:
        msg = 'Method "search" should be implemented'
        raise NotImplementedError(msg)

    @staticmethod
    def _get_contents(folder: Folder, files: list[File]) -> dict[File, Source]:
        contents = {}

        for file in files:
            path = os.path.abspath(os.path.join(folder, file))
            if path in file_contents_cached:
                contents[file] = file_contents_cached[path]
            elif os.path.exists(path):
                with open(path, encoding="utf-8") as f:
                    try:
                        file_content = f.read()
                    except UnicodeDecodeError:
                        # binary bile, no need to process
                        continue
                    contents[file] = file_content
                    file_contents_cached[path] = contents[file]

        return contents

    def _search_non_cached(
        self,
        where_to_search: str,
        *,
        file_filter: FileFilter,
        pre_main_filter: FileFilter,
        main_filter: MainFilter,
        post_main_filter: FileFilter,
        force_content_filters: list[MainFilter] | None = None,
    ) -> RunnableFile:
        if not force_content_filters:
            force_content_filters = []

        curr_folder = os.path.abspath(where_to_search)

        for folder, _dirs, files in walk_user_files(curr_folder):
            contents = self._get_contents(folder, files)

            initial_filter = FileFilter(
                file=lambda f: f.endswith(self.extension), generic=file_filter.filter
            )

            candidates = set(files)

            for curr_filter in initial_filter, pre_main_filter, main_filter, post_main_filter:
                curr_filter.init_filter(folder, contents)

                filtered_files: set[File] = {
                    file
                    for file in files
                    if file in contents and curr_filter.filter(folder, file, contents[file])
                }

                curr_filter.filtered = filtered_files

                if len(filtered_files) == 0:
                    if curr_filter == initial_filter:
                        break
                    continue
                if curr_filter == initial_filter:
                    for forced_filter in force_content_filters:
                        filtered_files = {
                            file
                            for file in filtered_files
                            if file in contents
                            and forced_filter.filter(folder, file, contents[file])
                        }
                    if len(filtered_files) == 0:
                        should_contain = [
                            forced_filter.program_should_contain
                            for forced_filter in force_content_filters
                            if isinstance(forced_filter, MainFilter)
                        ]
                        msg = f"The runnable file should contain all the following lines: {should_contain}"
                        raise ErrorWithFeedback(msg)

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
                str_files = ", ".join(f'"{f}"' for f in sorted(candidates))
                all_have = []
                if main_filter.program_should_contain:
                    all_have.append(main_filter.program_should_contain)
                all_have.extend(
                    [
                        forced_filter.program_should_contain
                        for forced_filter in force_content_filters
                        if isinstance(forced_filter, MainFilter)
                    ]
                )
                msg = (
                    f"Cannot decide which file to run out of the following: {str_files}\n"
                    f"They all have {all_have}. "
                    f"Leave one file with this lines."
                )
                raise ErrorWithFeedback(msg)

            if len(candidates) == 0:
                candidates = initial_filter.filtered

            str_files = ", ".join(f'"{f}"' for f in sorted(candidates))

            msg = (
                f"Cannot decide which file to run out of the following: {str_files}\n"
                f'Write "{main_filter.program_should_contain}" '
                f"in one of them to mark it as an entry point."
            )
            raise ErrorWithFeedback(msg)

        msg = (
            "Cannot find a file to execute your code.\n"
            f'Are your project files located at "{curr_folder}"?'
        )
        raise ErrorWithFeedback(msg)

    def _search(
        self,
        where_to_search: str | None = None,
        *,
        file_filter: FileFilter = None,
        pre_main_filter: FileFilter = None,
        main_filter: MainFilter = None,
        post_main_filter: FileFilter = None,
        force_content_filters: list[MainFilter] | None = None,
    ) -> RunnableFile:
        if not self.extension.startswith("."):
            msg = f'File extension "{self.extension}" should start with a dot'
            raise UnexpectedError(msg)

        if where_to_search is None:
            where_to_search = os.getcwd()

        do_caching = False
        cache_key = self.extension, where_to_search

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

        result = self._search_non_cached(
            where_to_search,
            file_filter=file_filter,
            pre_main_filter=pre_main_filter,
            main_filter=main_filter,
            post_main_filter=post_main_filter,
            force_content_filters=force_content_filters,
        )

        if do_caching:
            search_cached[cache_key] = result

        return result

    def _simple_search(
        self,
        where_to_search: str,
        main_desc: str,
        main_regex: str,
        force_content_filters: list[MainFilter] | None = None,
    ) -> RunnableFile:
        main_searcher = re.compile(main_regex, re.MULTILINE)
        return self._search(
            where_to_search,
            main_filter=MainFilter(main_desc, source=lambda s: main_searcher.search(s) is not None),
            force_content_filters=force_content_filters,
        )

    def _base_search(self, where_to_search: str) -> RunnableFile:
        return self._simple_search(where_to_search, main_desc="", main_regex="")

    def find(self, source: str | None) -> RunnableFile:
        if source in {None, ""}:
            return self.search()

        ext = self.extension

        source_folder, source_file, source_module = self._parse_source(source)

        if source_folder is not None and os.path.isdir(source_folder):
            return self.search(source_folder)

        if source_file is not None and os.path.isfile(source_file):
            path, _sep, file = source_module.rpartition(".")
            folder = os.path.abspath(path.replace(".", os.sep))
            return RunnableFile(folder, file + ext)

        path, _, _ = source_module.rpartition(".")
        folder = os.path.abspath(path.replace(".", os.sep))
        msg = (
            "Cannot find a file to execute your code.\n"
            f'Are your project files located at "{folder}"?'
        )
        raise ErrorWithFeedback(msg)

    def _parse_source(self, source: str) -> tuple[Folder, File, Module]:
        ext = self.extension

        source = source.replace("/", os.sep).replace("\\", os.sep)

        if source.endswith(ext):
            source_folder = None
            source_file = source
            source_module = source[: -len(ext)].replace(os.sep, ".")

        elif os.sep in source:
            source = source.removesuffix(os.sep)

            source_folder = source
            source_file = None
            source_module = source.replace(os.sep, ".")

        else:
            source_folder = source.replace(".", os.sep)
            source_file = source_folder + ext
            source_module = source

        return source_folder, source_file, source_module
