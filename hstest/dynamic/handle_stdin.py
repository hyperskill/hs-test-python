import io
import sys
from typing import List
from hstest.dynamic.stdin import InputMock
from hstest.dynamic.stdin import DynamicInputFunction


class StdinHandler:
    real_stdin: io.TextIOWrapper = sys.stdin
    mock_stdin: InputMock = InputMock()

    @staticmethod
    def replace_stdin():
        sys.stdin = StdinHandler.mock_stdin

    @staticmethod
    def revert_stdin():
        sys.stdin = StdinHandler.real_stdin

    @staticmethod
    def set_input(text: str):
        StdinHandler.mock_stdin.provide_text(text)

    @staticmethod
    def set_input_funcs(input_funcs: List[DynamicInputFunction]):
        StdinHandler.mock_stdin.set_texts([
            DynamicInputFunction(func.trigger_count, func.input_function)
            for func in input_funcs
        ])


