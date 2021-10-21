import os
from threading import Thread
from time import sleep
from typing import List, Optional

from hstest.dynamic.input.input_handler import InputHandler
from hstest.dynamic.output.output_handler import OutputHandler
from hstest.dynamic.security.exit_exception import ExitException
from hstest.dynamic.system_handler import SystemHandler
from hstest.exception.outcomes import CompilationError, ExceptionWithFeedback
from hstest.testing.execution.program_executor import ProgramExecutor, ProgramState
from hstest.testing.execution.runnable.runnable_file import RunnableFile
from hstest.testing.process_wrapper import ProcessWrapper


class ProcessExecutor(ProgramExecutor):
    compiled = False

    def __init__(self, runnable: RunnableFile):
        super().__init__()
        self.process: Optional[ProcessWrapper] = None
        self.thread = None
        self.continue_executing = True
        self.runnable: RunnableFile = runnable

    def _compilation_command(self, *args: str) -> List[str]:
        return []

    def _execution_command(self, *args: str) -> List[str]:
        raise NotImplementedError('Method "_execution_command" isn\'t implemented')

    def _cleanup(self):
        pass

    def __compile_program(self) -> bool:
        if ProcessExecutor.compiled:
            return True

        command = self._compilation_command()

        if not command:
            return True

        process = ProcessWrapper(*command, register_output=False)
        process.wait()

        if process.is_error_happened():
            error_lines = process.stderr.splitlines()
            error_lines = [line for line in error_lines if not line.startswith('#')]
            error_text = '\n'.join(error_lines)

            from hstest import StageTest
            StageTest.curr_test_run.set_error_in_test(CompilationError(error_text))
            self._machine.set_state(ProgramState.COMPILATION_ERROR)
            return False

        return True

    def __handle_process(self, *args: str):
        working_directory_before = os.path.abspath(os.getcwd())

        try:
            os.chdir(self.runnable.folder)

            if not self.__compile_program():
                return

            ProcessExecutor.compiled = True

            command = self._execution_command(*args)

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
        SystemHandler.install_handler(self, lambda: True)
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

    def tear_down(self):
        working_directory_before = os.path.abspath(os.getcwd())
        os.chdir(self.runnable.folder)

        try:
            self._cleanup()
        except BaseException:
            pass

        ProcessExecutor.compiled = False
        os.chdir(working_directory_before)

    def __str__(self) -> str:
        return self.runnable.file
