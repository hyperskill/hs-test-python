from hstest.check_result import correct
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.dynamic.output.infinite_loop_detector import loop_detector
from hstest.stage_test import StageTest
from hstest.testing.tested_program import TestedProgram


class InfiniteLoopTestNotWorking(StageTest):
    @dynamic_test
    def test(self):
        main = TestedProgram('main')
        main.start()
        return correct()

    def test_run_unittest(self):
        prev = loop_detector.working
        loop_detector.working = False

        try:
            super().test_run_unittest()
        finally:
            loop_detector.working = prev
