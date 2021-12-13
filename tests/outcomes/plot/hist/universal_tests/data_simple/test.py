import os
import unittest

from hstest import TestedProgram, correct, wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest


class TestMatplotlibHist(PlottingTest):
    @dynamic_test
    def test(self):
        files = [i for i in os.listdir() if i != 'test.py' and i.endswith('.py')]

        for file in files:
            program = TestedProgram(file)
            program.start()

            correct_data = [
                [1, 1], [2, 1], [3, 1], [4, 1], [5, 1]
            ]

            new_figures = self.new_figures()

            if len(new_figures) != 1:
                return wrong(f"Should be 1 plot, found {len(new_figures)}\n\n{file}")

            found_data = new_figures[0].data.tolist()

            if correct_data != found_data:
                return wrong(file + "\n\n" + str(found_data))

            if str(program) != file:
                return wrong("hs-test-python didn't run requested file")

            print('Histogram ' + file + ' OK')

        return correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestMatplotlibHist().run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
