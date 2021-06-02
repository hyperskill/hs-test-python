import inspect
import os
import traceback
from typing import List


def is_tests(stage):
    package = inspect.getmodule(stage).__package__
    file = inspect.getmodule(stage).__file__
    return package and package.startswith('tests.outcomes.') or \
        file and f'{os.sep}hs-test-python{os.sep}tests{os.sep}outcomes{os.sep}' in file


def setup_cwd(stage):
    test_file = inspect.getmodule(stage).__file__
    test_folder = os.path.dirname(test_file)
    os.chdir(test_folder)


def get_stacktrace(ex: BaseException, hide_internals=False) -> str:
    exc_tb = ex.__traceback__
    traceback_stack = traceback.format_exception(etype=type(ex), value=ex, tb=exc_tb)

    if not hide_internals:
        return ''.join(traceback_stack)

    if isinstance(ex, SyntaxError):
        if ex.filename.startswith('<'):  # "<string>", or "<module>"
            user_dir = ex.filename
        else:
            user_dir = os.path.dirname(ex.filename) + os.sep
    else:
        user_dir = ''

    user_traceback = []
    for tr in traceback_stack[::-1][1:-1]:
        if f'{os.sep}runpy.py"' in tr:
            break
        user_traceback += [tr]

    user_traceback = [tr for tr in user_traceback
                      if f'{os.sep}hstest{os.sep}' not in tr]

    return clean_stacktrace(traceback_stack, user_traceback[::-1], user_dir)


def str_to_stacktrace(str_trace: str) -> str:
    lines = str_trace.splitlines()
    traceback_lines = [i for i, line in enumerate(lines) if line.startswith('  File ')]

    if len(traceback_lines) < 1:
        return str_trace

    traceback_stack = []

    for line_num in traceback_lines:
        traceback_stack += [lines[line_num] + '\n' + lines[line_num + 1] + '\n']

    user_traceback = []
    for trace in traceback_stack:
        r'''
        Avoid traceback elements such as:
        
        File "C:\Users\**\JetBrains\**\plugins\python\helpers\pydev\pydevd.py", line 1477, in _exec
          pydev_imports.execfile(file, globals, locals)  # execute the script
        File "C:\Users\**\JetBrains\**\plugins\python\helpers\pydev\_pydev_imps\_pydev_execfile.py", line 18, in execfile
          exec(compile(contents+"\n", file, 'exec'), glob, loc) 
        
        Which will appear when testing locally inside PyCharm.
        '''
        if f'{os.sep}JetBrains{os.sep}' in trace:
            continue

        user_traceback += [trace]

    before = ['\n'.join(lines[:traceback_lines[0]]) + '\n']
    after = ['\n'.join(lines[traceback_lines[-1] + 2:]) + '\n']

    return clean_stacktrace(before + user_traceback + after, user_traceback)


def clean_stacktrace(full_traceback: List[str], user_traceback: List[str], user_dir: str = '') -> str:
    dir_names = []
    for tr in user_traceback:
        try:
            start_index = tr.index('"') + 1
            end_index = tr.index('"', start_index)
        except ValueError:
            continue

        user_file = tr[start_index: end_index]

        if user_file.startswith('<'):
            continue

        dir_name = os.path.dirname(tr[start_index: end_index])
        if os.path.isdir(dir_name):
            dir_names += [os.path.abspath(dir_name)]

    if dir_names:
        user_dir = os.path.commonpath(dir_names) + os.sep

    cleaned_traceback = []
    for trace in full_traceback[1:-1]:
        if trace.startswith(' ' * 4):
            # Trace line that starts with 4 is a line with SyntaxError
            cleaned_traceback += [trace]
        elif user_dir in trace or ('<' in trace and '>' in trace and '<frozen ' not in trace):
            # avoid including <frozen importlib...> lines that are always in the stacktrace
            # but include <string>, <module> because it's definitely user's code
            if not user_dir.startswith('<'):
                if user_dir in trace:
                    trace = trace.replace(user_dir, '')
                else:
                    folder_name = os.path.basename(user_dir[:-1])
                    if folder_name in trace:
                        index = trace.index(folder_name)
                        trace = '  File "' + trace[index + len(folder_name + os.sep):]

            cleaned_traceback += [trace]

    return full_traceback[0] + ''.join(cleaned_traceback) + full_traceback[-1]
