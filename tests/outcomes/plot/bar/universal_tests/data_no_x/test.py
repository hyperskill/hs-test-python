import os

from hstest import correct, TestedProgram, wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from tests.outcomes.plot.universal_test import universal_test


class TestBar(PlottingTest):
    @dynamic_test
    def test(self):
        files = [i for i in os.listdir() if i != 'test.py' and i.endswith('.py')]

        for file in files:
            program = TestedProgram(file)
            program.start()

            if str(program) != file:
                return wrong("hs-test-python didn't run requested file")

            universal_test(
                file,
                'bar',
                [[0, 1, 2, 3, 4]],
                [[1, 2, 3, 4, 5]],
                self.new_figures()
            )

        return correct()
