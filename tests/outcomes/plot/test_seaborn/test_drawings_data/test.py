import unittest

from hstest.check_result import correct, wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest import TestedProgram


class TestSeaborn(PlottingTest):
    @dynamic_test
    def test(self):
        import seaborn as sns
        import numpy as np
        import pandas as pd

        program = TestedProgram()
        program.start()

        if len(self.all_figures) != 10:
            return wrong(f'Expected 10 plots to be plotted using matplotlib library, found {len(self.all_figures)}')

        displot = self.all_figures[0]
        if displot.type != 'displot':
            return wrong(f'Wrong drawing type {displot.type}. Expected displot')

        if 'data' not in displot.data or 'kwargs' not in displot.data:
            return wrong(f"Expected 'data', 'kwargs' key in the data dict of the displot drawing")

        if type(displot.data['data']) != pd.DataFrame:
            return wrong(f"Wrong 'data' type {type(displot.data['data'])}. Expected {pd.DataFrame}")

        histplot = self.all_figures[1]
        if histplot.type != 'histplot':
            return wrong(f'Wrong drawing type {histplot.type}. Expected histplot')

        if 'data' not in histplot.data or 'kwargs' not in histplot.data:
            return wrong(f"Expected 'data', 'kwargs' key in the data dict of the histplot drawing")

        if type(histplot.data['data']) != pd.DataFrame:
            return wrong(f"Wrong 'data' type {type(histplot.data['data'])}. Expected {pd.DataFrame}")

        for drawing in self.all_figures:
            if drawing.library != 'seaborn':
                return wrong('Drawings plotted using wrong library!')

        lineplot = self.all_figures[2]
        if lineplot.type != 'lineplot':
            return wrong(f'Wrong drawing type {lineplot.type}. Expected lineplot')

        if 'data' not in lineplot.data or 'x' not in lineplot.data or 'y' not in lineplot.data or 'kwargs' not in lineplot.data:
            return wrong(f"Expected 'data', 'kwargs' key in the data dict of the lineplot drawing")

        if type(lineplot.data['data']) != pd.DataFrame:
            return wrong(f"Wrong 'data' type {type(lineplot.data['data'])}. Expected {pd.DataFrame}")

        if lineplot.data['x'] != 'flipper_length_mm':
            return wrong(f"Wrong 'x' value {lineplot.data['x']}. Expected 'flipper_length_mm'")

        if lineplot.data['y'] != 'flipper_length_mm':
            return wrong(f"Wrong 'y' value {lineplot.data['y']}. Expected 'flipper_length_mm'")

        lmplot = self.all_figures[3]
        if lmplot.type != 'lmplot':
            return wrong(f'Wrong drawing type {lmplot.type}. Expected lmplot')

        if 'data' not in lmplot.data or 'x' not in lmplot.data or 'y' not in lmplot.data or 'kwargs' not in lmplot.data:
            return wrong(f"Expected 'data', 'kwargs' key in the data dict of the lmplot drawing")

        if type(lmplot.data['data']) != pd.DataFrame:
            return wrong(f"Wrong 'data' type {type(lmplot.data['data'])}. Expected {pd.DataFrame}")

        if lmplot.data['x'] != 'flipper_length_mm':
            return wrong(f"Wrong 'x' value {lmplot.data['x']}. Expected 'flipper_length_mm'")

        if lmplot.data['y'] != 'flipper_length_mm':
            return wrong(f"Wrong 'y' value {lmplot.data['y']}. Expected 'flipper_length_mm'")

        scatterplot = self.all_figures[4]
        if scatterplot.type != 'scatterplot':
            return wrong(f'Wrong drawing type {scatterplot.type}. Expected scatterplot')

        if 'data' not in scatterplot.data or 'x' not in scatterplot.data or 'y' not in scatterplot.data or 'kwargs' not in scatterplot.data:
            return wrong(f"Expected 'data', 'kwargs' key in the data dict of the scatterplot drawing")

        if type(scatterplot.data['data']) != pd.DataFrame:
            return wrong(f"Wrong 'data' type {type(scatterplot.data['data'])}. Expected {pd.DataFrame}")

        if scatterplot.data['x'] != 'flipper_length_mm':
            return wrong(f"Wrong 'x' value {scatterplot.data['x']}. Expected 'flipper_length_mm'")

        if lmplot.data['y'] != 'flipper_length_mm':
            return wrong(f"Wrong 'y' value {scatterplot.data['y']}. Expected 'flipper_length_mm'")

        catplot = self.all_figures[5]
        if catplot.type != 'catplot':
            return wrong(f'Wrong drawing type {catplot.type}. Expected catplot')

        if 'data' not in catplot.data or 'x' not in catplot.data or 'y' not in catplot.data or 'kwargs' not in catplot.data:
            return wrong(f"Expected 'data', 'kwargs' key in the data dict of the catplot drawing")

        if type(catplot.data['data']) != pd.DataFrame:
            return wrong(f"Wrong 'data' type {type(catplot.data['data'])}. Expected {pd.DataFrame}")

        if catplot.data['x'] != 'species':
            return wrong(f"Wrong 'x' value {catplot.data['x']}. Expected 'flipper_length_mm'")

        if catplot.data['y'] != 'body_mass_g':
            return wrong(f"Wrong 'y' value {catplot.data['y']}. Expected 'body_mass_g'")

        barplot = self.all_figures[6]
        if barplot.type != 'barplot':
            return wrong(f'Wrong drawing type {barplot.type}. Expected barplot')

        if 'data' not in barplot.data or 'x' not in barplot.data or 'y' not in barplot.data or 'kwargs' not in barplot.data:
            return wrong(f"Expected 'data', 'kwargs' key in the data dict of the barplot drawing")

        x = np.array(list("ABCDEFGHIJ"))
        y = np.arange(1, 11)

        if list(barplot.data['x']) != list(x):
            return wrong(f"Wrong 'x' value {barplot.data['x']}. Expected {x}")

        if list(barplot.data['y']) != list(y):
            return wrong(f"Wrong 'y' value {barplot.data['y']}. Expected {y}")

        violinplot = self.all_figures[7]
        if violinplot.type != 'violinplot':
            return wrong(f'Wrong drawing type {violinplot.type}. Expected barplot')

        if 'data' not in violinplot.data or 'x' not in violinplot.data or 'y' not in violinplot.data or 'kwargs' not in violinplot.data:
            return wrong(f"Expected 'data', 'kwargs' key in the data dict of the barplot drawing")

        if type(violinplot.data['data']) != pd.DataFrame:
            return wrong(f"Wrong 'data' type {type(violinplot.data['data'])}. Expected {pd.DataFrame}")

        kwargs = violinplot.data['kwargs']

        if 'palette' not in kwargs or 'bw' not in kwargs or 'cut' not in kwargs or 'linewidth' not in kwargs:
            return wrong("Can't find 'palette', 'bw', 'cut', 'linewidth' keys in kwargs!")

        heatmap = self.all_figures[8]
        if heatmap.type != 'heatmap':
            return wrong(f'Wrong drawing type {heatmap.type}. Expected barplot')

        if 'data' not in heatmap.data or 'kwargs' not in heatmap.data:
            return wrong(f"Expected 'data', 'kwargs' key in the data dict of the barplot drawing")

        if type(heatmap.data['data']) != pd.DataFrame:
            return wrong(f"Wrong 'data' type {type(heatmap.data['data'])}. Expected {pd.DataFrame}")

        kwargs = heatmap.data['kwargs']

        if 'annot' not in kwargs or 'fmt' not in kwargs or 'linewidths' not in kwargs or 'ax' not in kwargs:
            return wrong("Can't find 'annot', 'fmt', 'linewidths', 'ax' keys in kwargs!")

        boxplot = self.all_figures[9]
        if boxplot.type != 'boxplot':
            return wrong(f'Wrong drawing type {boxplot.type}. Expected barplot')

        if 'data' not in boxplot.data or 'kwargs' not in boxplot.data:
            return wrong(f"Expected 'data', 'kwargs' key in the data dict of the boxplot drawing")

        if type(boxplot.data['data']) != pd.DataFrame:
            return wrong(f"Wrong 'data' type {type(boxplot.data['data'])}. Expected {pd.DataFrame}")

        kwargs = boxplot.data['kwargs']

        if 'hue' not in kwargs or 'palette' not in kwargs:
            return wrong("Can't find 'hue', 'palette' keys in kwargs!")

        if 'x' not in boxplot.data or boxplot.data['x'] != 'day':
            return wrong("Can't find 'x' key in the data or it has wrong value. Expected value 'day'")

        if 'y' not in boxplot.data or boxplot.data['y'] != 'total_bill':
            return wrong("Can't find 'y' key in the data or it has wrong value. Expected value 'total_bill'")

        for drawing in self.all_figures:
            if drawing.library != 'seaborn':
                return wrong('Drawings plotted using wrong library!')

        return correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestSeaborn('main').run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
