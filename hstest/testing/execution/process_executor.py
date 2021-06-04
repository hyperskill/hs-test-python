import os
from threading import Thread
from time import sleep
from typing import Optional

from hstest.dynamic.input.input_handler import InputHandler
from hstest.dynamic.output.output_handler import OutputHandler
from hstest.dynamic.security.exit_exception import ExitException
from hstest.exception.outcomes import ExceptionWithFeedback
from hstest.testing.execution.program_executor import ProgramExecutor, ProgramState
from hstest.testing.execution.searcher.python_searcher import find_python_by_nothing, find_python_by_source_name
from hstest.testing.process_wrapper import ProcessWrapper


class ProcessExecutor(ProgramExecutor):
    def __init__(self, source_name: str = None):
        super().__init__()
        self.args = ['python', '-u']
        self.process: Optional[ProcessWrapper] = None
        self.thread = None
        self.continue_executing = True

        if source_name is None:
            from hstest.stage_test import StageTest
            source_name = StageTest.curr_test_run.test_case.source_name

        if source_name is None:
            self.runnable = find_python_by_nothing()
        else:
            self.runnable = find_python_by_source_name(source_name)

    def __handle_process(self, *args: str):
        working_directory_before = os.path.abspath(os.getcwd())

        try:
            os.chdir(self.runnable.folder)

            command = self.args + [self.runnable.file] + list(args)

            self._machine.set_state(ProgramState.RUNNING)
            self.process = ProcessWrapper(*command)

            while self.continue_executing:
                OutputHandler.print('Handle process - one iteration')
                sleep(0.001)

                if self.process.is_finished():
                    OutputHandler.print('Handle process - finished, breaking')
                    break

                is_input_allowed = self.is_input_allowed()
                is_waiting_input = self.process.is_waiting_input()

                OutputHandler.print(f'Handle process - '
                                    f'input allowed {is_input_allowed}, '
                                    f'waiting input {is_waiting_input}')

                if is_input_allowed and is_waiting_input:
                    OutputHandler.print(f'Handle process - registering input request')
                    self.process.register_input_request()

                    try:
                        OutputHandler.print(f'Handle process - try readline')
                        next_input = InputHandler.mock_in.readline()
                        OutputHandler.print(f'Handle process - requested input: {repr(next_input)}')
                        self.process.process.stdin.write(next_input)
                        OutputHandler.print(f'Handle process - written to stdin: {repr(next_input)}')
                    except ExitException:
                        OutputHandler.print('Handle process - EXIT EXCEPTION, stop input')
                        self.stop_input()
                    except BaseException as ex:
                        OutputHandler.print(f'Handle process - SOME EXCEPTION {ex}')

            OutputHandler.print(f'Handle process - TERMINATE')
            self.process.terminate()

            is_error_happened = self.process.is_error_happened()
            OutputHandler.print('Handle process - after termination')
            OutputHandler.print(f'Handle process - is error happened {is_error_happened}')

            from hstest import StageTest

            if StageTest.curr_test_run.error_in_test is not None:
                OutputHandler.print('Handle process - set state EXCEPTION THROWN (ERROR IN TEST)')
                self._machine.set_state(ProgramState.EXCEPTION_THROWN)

            elif is_error_happened:
                OutputHandler.print('Handle process - set state EXCEPTION THROWN (REALLY EXCEPTION)')
                StageTest.curr_test_run.set_error_in_test(ExceptionWithFeedback(self.process.stderr, None))
                self._machine.set_state(ProgramState.EXCEPTION_THROWN)

            else:
                OutputHandler.print('Handle process - set state FINISHED')
                self._machine.set_state(ProgramState.FINISHED)

            OutputHandler.print('Handle process - finishing execution')

        finally:
            os.chdir(working_directory_before)

    def _launch(self, *args: str):
        InputHandler.set_dynamic_input_func(lambda: self._request_input())
        self.thread = Thread(target=lambda: self.__handle_process(*args), daemon=True)
        self.thread.start()

    def _terminate(self):
        self.continue_executing = False
        self.process.terminate()
        OutputHandler.print(f'TERMINATE {self.is_finished()}')
        while not self.is_finished():
            if self.is_waiting_input():
                self._machine.set_state(ProgramState.RUNNING)
            OutputHandler.print(f'NOT FINISHED {self._machine.state}')
            sleep(0.001)

    def get_output(self) -> str:
        OutputHandler.print('Process executor - get_output()')
        return OutputHandler.get_partial_output()

    def __str__(self) -> str:
        return self.runnable.file
