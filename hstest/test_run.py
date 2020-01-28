from typing import Optional


class TestRun:
    curr_test_run: Optional['TestRun'] = None

    def __init__(self, test_num: int, test_case):
        self.test_num: int = test_num
        self.test_case = test_case
        self.input_used: bool = False
        self.error_in_test: Optional[BaseException] = None
