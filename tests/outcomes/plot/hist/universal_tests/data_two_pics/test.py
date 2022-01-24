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
                [1, 3, 5, 7, 9],
                [2, 4, 6, 8, 10],
            ]

            new_figures = self.new_figures()

            if len(new_figures) != 2:
                return wrong(f"Should be 2 plots, found {len(new_figures)}\n\n{file}")

            for i in range(2):
                found_data = new_figures[i].data.tolist()

                if correct_data[i] != found_data:
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
