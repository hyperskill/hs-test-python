import sys
import runpy
import os
import io
import importlib
import signal
import builtins
import traceback
from typing import List, Any, Dict, Tuple
from hstest.test_helper import *
from hstest.test_case import TestCase
from hstest.check_result import CheckResult
from hstest.exceptions import *


class StageTest:

    real_stdin = None
    real_print = None
    real_input = None
    user_output: io.StringIO = None

    @staticmethod
    def remove_kill_methods():
        os.kill = lambda *x, **y: exit(0)
        os._exit = lambda *x, **y: exit(0)
        os.killpg = lambda *x, **y: exit(0)
        signal.pthread_kill = lambda *x, **y: exit(0)
        signal.siginterrupt = lambda *x, **y: exit(0)

    @staticmethod
    def set_input(user_input: str):
        sys.stdin = io.StringIO(user_input)

    @staticmethod
    def add_input(user_input: str):
        sys.stdin: io.StringIO
        curr_position = sys.stdin.seek(0, io.SEEK_CUR)
        sys.stdin.seek(0)
        sys.stdin = io.StringIO(sys.stdin.read() + user_input)
        sys.stdin.seek(curr_position)

    @staticmethod
    def print(*args, **kwargs):
        StageTest.real_print(*args, **kwargs)
        StageTest.real_print(*args, **kwargs, file=StageTest.user_output)

    @staticmethod
    def input(arg=''):
        StageTest.print(arg, end='')
        user_input = StageTest.real_input()
        # StageTest.print()
        return user_input

    @staticmethod
    def replace_globals():
        StageTest.real_stdin = sys.stdin
        StageTest.real_print = builtins.print
        StageTest.real_input = builtins.input
        builtins.print = StageTest.print
        builtins.input = StageTest.input

    @staticmethod
    def revert_globals():
        sys.stdin = StageTest.real_stdin
        builtins.print = StageTest.real_print
        builtins.input = StageTest.real_input

    @staticmethod
    def get_print_back():
        builtins.print = StageTest.real_print
        sys.stdin = StageTest.real_stdin

    def __init__(self, module_to_test: str):
        self.remove_kill_methods()
        self.replace_globals()
        self.module_to_test = module_to_test
        self.this_test_file = __file__
        self.file_to_test = module_to_test.replace('.', os.sep) + '.py'
        self.full_file_to_test = ''
        self.tests: List[TestCase] = []

    def reset(self):
        StageTest.user_output = io.StringIO()
        top_module = self.module_to_test[:self.module_to_test.rindex('.')]
        for name, module in list(sys.modules.items()):
            if name.startswith(top_module):
                importlib.reload(module)

    @staticmethod
    def create_files(files: Dict[str, str]):
        for file, content in files.items():
            with open(file, 'w') as f:
                f.write(content)

    @staticmethod
    def delete_files(files: Dict[str, str]):
        for file in files.keys():
            if os.path.isfile(file):
                os.remove(file)

    def run(self):
        runpy.run_module(
            self.module_to_test,
            run_name="__main__"
        )

    def test(self, test_case: TestCase) -> str:
        self.reset()
        try:
            self.create_files(test_case.files)
            sys.argv = [self.file_to_test] + test_case.args
            self.set_input(test_case.input)
            self.run()
            self.delete_files(test_case.files)
            return StageTest.user_output.getvalue()

        except SyntaxError as e:

            file = e.filename
            file = file.replace(os.sep, '.')
            file = file[file.index(self.module_to_test):-3]
            file = file.replace('.', os.sep) + '.py'

            output = f'File "{file}", line {e.lineno}\n' \
                     + e.text.strip()[: e.offset-1] + '\n' \
                     'SyntaxError: invalid syntax'

            # '`' * (e.offset - 2) + '^'

            raise SyntaxException(output)

        except (SystemExit, KeyboardInterrupt):
            raise ExitException('Tried to exit.')

    def generate(self) -> List[TestCase]:
        raise NotImplementedError('Can\'t create tests: override "generate" method')

    def check(self, reply: str, attach: Any) -> CheckResult:
        raise NotImplementedError('Can\'t check result: override "check" method')

    def after_all_tests(self):
        pass

    def get_stacktrace(self, hide_internals, skipped_traces=0):

        if self.full_file_to_test != '':
            common_prefix = os.path.commonpath([
                self.full_file_to_test, self.this_test_file
            ])
        else:
            common_prefix = ''

        exc_type, exc_obj, exc_tb = sys.exc_info()

        if hide_internals and skipped_traces != 0:
            traceback_msg = 'Traceback (most recent call last):\n'
        else:
            traceback_msg = ''

        for line in traceback.TracebackException(
                type(exc_obj), exc_obj, exc_tb, limit=None).format(chain=None):
            if not hide_internals:
                traceback_msg += line
            elif skipped_traces >= 0:
                skipped_traces -= 1
            elif self.this_test_file not in line:
                traceback_msg += line.replace(common_prefix + os.sep, '')

        return traceback_msg

    def run_tests(self) -> Tuple[int, str]:

        test_number = 0
        try:
            tests = self.generate()
            if len(tests) == 0:
                raise Exception('No tests provided by "generate" method')

            for test in tests:
                test_number += 1
                reply = self.test(test)
                result = self.check(reply, test.attach)
                if not result.result:
                    fail_msg = f'Wrong answer in test #{test_number}'
                    self.revert_globals()
                    return failed(fail_msg + '\n\n' + result.feedback)
            self.revert_globals()
            return passed()

        except SyntaxException as ex:
            self.revert_globals()
            return failed(ex.message)

        except ExitException as ex:
            error_msg = f'Error in test #{test_number}'
            self.revert_globals()
            return failed(error_msg + '\n\n' + ex.message)

        except Exception:

            exc_type, exc_obj, exc_tb = sys.exc_info()
            trace_frames = []

            user_trace_started = False
            skipped_traces = 0
            while exc_tb is not None:
                code = exc_tb.tb_frame.f_code
                filename = code.co_filename

                if filename.endswith(self.file_to_test) and not user_trace_started:
                    user_trace_started = True
                    self.full_file_to_test = exc_tb.tb_frame.f_code.co_filename

                if user_trace_started:
                    trace_frames += [exc_tb.tb_frame.f_code]
                else:
                    skipped_traces += 1

                exc_tb = exc_tb.tb_next

            if not trace_frames:
                if test_number == 0:
                    when_error_happened = ' during testing'
                else:
                    when_error_happened = f' in test #{test_number}'
                exception_msg = (
                    f"Fatal error{when_error_happened}, " +
                    "please send the report to Hyperskill team."
                )
                stacktrace = self.get_stacktrace(hide_internals=False)

            else:
                exception_msg = f'Exception in test #{test_number}'
                stacktrace = self.get_stacktrace(
                    hide_internals=True,
                    skipped_traces=skipped_traces
                )

            self.revert_globals()
            return failed(exception_msg + '\n\n' + stacktrace)
        finally:
            self.after_all_tests()
