import io
import sys
from typing import List

from hstest.dynamic.input.dynamic_input_func import DynamicTestFunction, DynamicInputFunction
from hstest.dynamic.input.input_mock import InputMock


class InputHandler:
    real_in: io.TextIOWrapper = sys.stdin
    mock_in: InputMock = InputMock()

    @staticmethod
    def replace_input():
        sys.stdin = InputHandler.mock_in

    @staticmethod
    def revert_input():
        sys.stdin = InputHandler.real_in

    @staticmethod
    def set_dynamic_input_func(func: DynamicTestFunction):
        InputHandler.mock_in.set_dynamic_input_func(func)

    @staticmethod
    def set_input(text: str):
        """
        Deprecated
        """
        InputHandler.mock_in.provide_text(text)

    @staticmethod
    def set_input_funcs(input_funcs: List[DynamicInputFunction]):
        """
        Deprecated
        """
        InputHandler.mock_in.set_texts([
            DynamicInputFunction(func.trigger_count, func.input_function)
            for func in input_funcs
        ])
