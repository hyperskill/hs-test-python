import sys
import runpy
import os
import importlib
import concurrent.futures.thread
from concurrent.futures import ThreadPoolExecutor, Future, TimeoutError
from typing import List, Any, Dict, Tuple
from hstest.utils import failed, passed
from hstest.test_case import TestCase
from hstest.check_result import CheckResult
from hstest.exceptions import *
from hstest.outcomes import Outcome
from hstest.dynamic.handle import SystemHandler
from hstest.dynamic.handle_stdout import StdoutHandler
from hstest.dynamic.handle_stdin import StdinHandler
from hstest.test_run import TestRun


class StageTest:
    module = ''

    def __init__(self, method: str):
        # super().__init__(method)
        self.module = method

        self.module_to_test = self.module
        self.this_test_file = __file__
        self.file_to_test = self.module.replace('.', os.sep) + '.py'
        self.full_file_to_test = ''
        self.need_reload = True

    def reset(self):
        top_module = self.module_to_test[:self.module_to_test.rindex('.')]
        for name, module in list(sys.modules.items()):
            if name.startswith(top_module):
                importlib.reload(module)

    def test_program(self):
        result, feedback = self.run_tests()
        if result != 0:
            self.fail(feedback)

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

    def generate(self) -> List[TestCase]:
        raise UnexpectedError('Can\'t create tests: override "generate" method')

    def check(self, reply: str, attach: Any) -> CheckResult:
        raise UnexpectedError('Can\'t check result: override "check" method')

    def after_all_tests(self):
        pass

    def _exec_file(self, args: List[str]):
        if self.need_reload:
            try:
                self.reset()
            except BaseException as ex:
                TestRun.curr_test_run.error_in_test = ex
        try:
            sys.argv = [self.file_to_test] + args
            runpy.run_module(
                self.module_to_test,
                run_name="__main__"
            )
        except ImportError as ex:
            TestRun.curr_test_run.error_in_test = UnexpectedError(
                f'Cannot find file {self.file_to_test}', ex)
        except SyntaxError as ex:
            TestRun.curr_test_run.error_in_test = SyntaxException(
                ex, self.file_to_test)
        except BaseException as ex:
            if TestRun.curr_test_run.error_in_test is None:
                # ExitException is thrown in case of exit() or quit()
                # consider them like normal exit
                if not isinstance(ex, ExitException):
                    TestRun.curr_test_run.error_in_test = ExceptionWithFeedback('', ex)

    def _run_file(self, args: List[str], time_limit: int):
        executor = ThreadPoolExecutor(max_workers=1)
        try:
            future: Future = executor.submit(lambda: self._exec_file(args))
            # Without this the Python interpreter cannot stop when the user writes an infinite loop
            # Even though all threads in ThreadPoolExecutor are created as daemon threads
            # They are not stopped on Python's shutdown but Python waits for them to stop on their own
            # See https://stackoverflow.com/a/49992422/13160001
            del concurrent.futures.thread._threads_queues[list(executor._threads)[0]]
            if time_limit <= 0:
                future.result()
            else:
                future.result(timeout=time_limit / 1000)
        except TimeoutError:
            TestRun.curr_test_run.error_in_test = TimeLimitException(time_limit)
        except BaseException as ex:
            TestRun.curr_test_run.error_in_test = ex
        finally:
            executor.shutdown(wait=False)

    def _run_test(self, test: TestCase) -> str:
        StdinHandler.set_input_funcs(test.input_funcs)
        StdoutHandler.reset_output()
        TestRun.curr_test_run.error_in_test = None

        self._run_file(test.args, test.time_limit)
        self._check_errors(test)

        return StdoutHandler.get_output()

    def _check_errors(self, test: TestCase):
        if TestRun.curr_test_run.error_in_test is None:
            return

        error_in_test = TestRun.curr_test_run.error_in_test
        if isinstance(error_in_test, TestPassed):
            return

        if isinstance(error_in_test, ExceptionWithFeedback):
            user_exception = error_in_test.real_exception
            for exception, feedback in test.feedback_on_exception.items():
                ex_type = type(user_exception)
                if ex_type is not None and issubclass(ex_type, exception):
                    raise ExceptionWithFeedback(feedback, user_exception)

        raise error_in_test

    def _check_solution(self, test: TestCase, output: str):
        if isinstance(TestRun.curr_test_run.error_in_test, TestPassed):
            return CheckResult.correct()
        try:
            if test.check_function is not None:
                return test.check_function(output, test.attach)
            else:
                return self.check(output, test.attach)
        except WrongAnswer as ex:
            return CheckResult.wrong(ex.feedback)
        except TestPassed:
            return CheckResult.correct()

    def run_tests(self, debug=False) -> Tuple[int, str]:
        if debug:
            import hstest.utils as hs
            hs.failed_msg_start = ''
            hs.failed_msg_continue = ''
            hs.success_msg = ''

        curr_test: int = 0
        try:
            SystemHandler.set_up()
            tests = self.generate()
            if len(tests) == 0:
                raise UnexpectedError('No tests provided by "generate" method')

            for test in tests:
                curr_test += 1

                red_bold = '\033[1;31m'
                reset = '\033[0m'
                StdoutHandler.real_stdout.write(
                    red_bold + f'\nStart test {curr_test}' + reset + '\n'
                )

                TestRun.curr_test_run = TestRun(curr_test, test)

                self.create_files(test.files)

                output: str = self._run_test(test)
                result: CheckResult = self._check_solution(test, output)

                self.delete_files(test.files)

                if not result.result:
                    raise WrongAnswer(result.feedback)

            return passed()

        except BaseException as ex:
            outcome: Outcome = Outcome.get_outcome(ex, self, curr_test)
            fail_text = str(outcome)
            return failed(fail_text)

        finally:
            StageTest.curr_test_run = None
            self.after_all_tests()
            SystemHandler.tear_down()
