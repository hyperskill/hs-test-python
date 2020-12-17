import unittest

from hstest.check_result import correct
from hstest.common.reflection_utils import get_main
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.dynamic.output.infinite_loop_detector import loop_detector
from hstest.stage_test import StageTest
from hstest.testing.tested_program import TestedProgram


class InfiniteLoopTestNotWorking(StageTest):
    @dynamic_test
    def test(self):
        main = TestedProgram(get_main())
        main.start()
        return correct()


class Test(unittest.TestCase):
    def test(self):
        prev = loop_detector.working
        loop_detector.working = False

        try:
            status, feedback = InfiniteLoopTestNotWorking().run_tests()
            self.assertEqual(
                "test OK",
                feedback)
            self.assertEqual(status, 0)
        finally:
            loop_detector.working = prev


if __name__ == '__main__':
    Test().test()
