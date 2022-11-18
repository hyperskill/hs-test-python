import os

from hstest.exception.outcomes import CompilationError
from hstest.testing.execution.process_executor import ProcessExecutor
from hstest.testing.execution.program_executor import ProgramState
from hstest.testing.execution.searcher.typescript_searcher import TypeScriptSearcher
from hstest.testing.process_wrapper import ProcessWrapper


class TypeScriptExecutor(ProcessExecutor):
    def __init__(self, source_name: str = None):
        super().__init__(TypeScriptSearcher().find(source_name))

    def _compilation_command(self):
        return ['tsc']

    def _compile_program(self) -> bool:
        if ProcessExecutor.compiled:
            return True

        command = self._compilation_command()

        if not command:
            return True

        process = ProcessWrapper(*command, register_output=False).start()
        process.wait()
        process.stderr += process.stdout

        if process.is_error_happened():
            error_text = self._filter_compilation_error(process.stderr)

            from hstest import StageTest
            StageTest.curr_test_run.set_error_in_test(CompilationError(error_text))
            self._machine.set_state(ProgramState.COMPILATION_ERROR)
            return False

        return True

    def _filter_compilation_error(self, error: str) -> str:
        error_lines = [line for line in error.splitlines() if not line.startswith('#')]
        return '\n'.join(error_lines)

    def _execution_command(self, *args: str):
        return ['node', self.runnable.file.replace('.ts', '.js')] + list(args)

    def _cleanup(self):
        if os.path.exists(self.runnable.file.replace('.ts', '.js')):
            os.remove(self.runnable.file.replace('.ts', '.js'))
