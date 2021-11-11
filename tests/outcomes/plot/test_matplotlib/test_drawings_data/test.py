import unittest

from hstest.check_result import correct, wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest import TestedProgram


class TestMatplotlib(PlottingTest):
    @dynamic_test
    def test(self):
        import matplotlib

        program = TestedProgram()
        program.start()

        if len(self.all_figures) != 18:
            return wrong(f'Expected 18 plots to be plotted using matplotlib library, found {len(self.all_figures)}')

        # hist

        hist1 = self.all_figures[0]
        if hist1.type != 'hist':
            return wrong(f'Wrong drawing type {hist1.type}. Expected hist')

        if 'x' not in hist1.data:
            return wrong(f"Expected 'x' key in the data dict of the hist drawing")

        if hist1.data['x'] != [1, 2]:
            return wrong(f"Wrong 'x' value {hist1.data['x']}. Expected [1,2]")

        hist2 = self.all_figures[1]
        if hist2.type != 'hist':
            return wrong(f'Wrong drawing type {hist2.type}. Expected hist')

        if 'x' not in hist2.data:
            return wrong(f"Expected 'x' key in the data dict of the hist drawing")

        if hist2.data['x'] != [1, 5]:
            return wrong(f"Wrong 'x' value {hist2.data['x']}. Expected [1,5]")

        for drawing in self.all_figures:
            if drawing.library != 'matplotlib':
                return wrong('Drawings plotted using wrong library!')

        # plot

        plot1 = self.all_figures[2]
        if plot1.type != 'plot':
            return wrong(f'Wrong drawing type {plot1.type}. Expected plot')

        if 'args' not in plot1.data:
            return wrong(f"Expected 'args' key in the data dict of the plot drawing")

        if plot1.data['args'] != ([1, 2], [5, 8]):
            return wrong(f"Wrong 'args' value {plot1.data['args']}. Expected ([1, 2], [5, 8])")

        plot2 = self.all_figures[3]
        if plot2.type != 'plot':
            return wrong(f'Wrong drawing type {plot2.type}. Expected plot')

        if 'args' not in plot2.data:
            return wrong(f"Expected 'args' key in the data dict of the plot drawing")

        if plot2.data['args'] != ([1, 5], [5, 8]):
            return wrong(f"Wrong 'args' value {plot2.data['args']}. Expected ([1, 5], [5, 8])")

        for drawing in self.all_figures:
            if drawing.library != 'matplotlib':
                return wrong('Drawings plotted using wrong library!')

        # scatter

        scatter1 = self.all_figures[4]
        if scatter1.type != 'scatter':
            return wrong(f'Wrong drawing type {scatter1.type}. Expected scatter')

        if 'x' not in scatter1.data or 'y' not in scatter1.data:
            return wrong(f"Expected 'x', 'y' keys in the data dict of the scatter drawing")

        if scatter1.data['x'] != [1, 2]:
            return wrong(f"Wrong 'x' value {scatter1.data['x']}. Expected [1, 2]")

        if scatter1.data['y'] != [2, 6]:
            return wrong(f"Wrong 'y' value {scatter1.data['y']}. Expected [2, 6]")

        scatter2 = self.all_figures[5]
        if scatter2.type != 'scatter':
            return wrong(f'Wrong drawing type {scatter2.type}. Expected scatter')

        if 'x' not in scatter2.data or 'y' not in scatter2.data:
            return wrong(f"Expected 'x', 'y' keys in the data dict of the scatter drawing")

        if scatter2.data['x'] != [1, 5]:
            return wrong(f"Wrong 'x' value {scatter2.data['x']}. Expected [1, 5]")

        if scatter2.data['y'] != [3, 8]:
            return wrong(f"Wrong 'y' value {scatter2.data['y']}. Expected [3, 8]")

        # pie

        pie1 = self.all_figures[6]
        if pie1.type != 'pie':
            return wrong(f'Wrong drawing type {pie1.type}. Expected pie')

        if 'x' not in pie1.data:
            return wrong(f"Expected 'x' key in the data dict of the pie drawing")

        if pie1.data['x'] != [1, 2]:
            return wrong(f"Wrong 'x' value {pie1.data['x']}. Expected [1, 2]")

        pie2 = self.all_figures[7]
        if pie2.type != 'pie':
            return wrong(f'Wrong drawing type {pie2.type}. Expected pie')

        if 'x' not in pie2.data:
            return wrong(f"Expected 'x' key in the data dict of the pie drawing")

        if pie2.data['x'] != [1, 3]:
            return wrong(f"Wrong 'x' value {pie2.data['x']}. Expected [1, 3]")

        # bar

        bar1 = self.all_figures[8]
        if bar1.type != 'bar':
            return wrong(f'Wrong drawing type {bar1.type}. Expected bar')

        if 'x' not in bar1.data or 'height' not in bar1.data or 'kwargs' not in bar1.data:
            return wrong(f"Expected 'x', 'height', 'kwargs' keys in the data dict of the bar drawing")

        if bar1.data['x'] != [1, 2, 4, 6]:
            return wrong(f"Wrong 'x' value {bar1.data['x']}. Expected [1, 2, 4, 6]")

        if bar1.data['height'] != 100:
            return wrong(f"Wrong 'height' value {bar1.data['height']}. Expected 100")

        bar2 = self.all_figures[9]
        if bar2.type != 'bar':
            return wrong(f'Wrong drawing type {bar2.type}. Expected bar')

        if 'x' not in bar2.data or 'height' not in bar2.data or 'kwargs' not in bar2.data:
            return wrong(f"Expected 'x', 'height', 'kwargs' keys in the data dict of the bar drawing")

        if bar2.data['x'] != [1, 2, 4, 7]:
            return wrong(f"Wrong 'x' value {bar2.data['x']}. Expected [1, 2, 4, 7]")

        if bar2.data['height'] != 200:
            return wrong(f"Wrong 'height' value {bar2.data['height']}. Expected 200")

        # barh

        barh1 = self.all_figures[10]
        if barh1.type != 'barh':
            return wrong(f'Wrong drawing type {barh1.type}. Expected barh')

        if 'y' not in barh1.data or 'width' not in barh1.data or 'kwargs' not in barh1.data:
            return wrong(f"Expected 'y', 'width', 'kwargs' keys in the data dict of the barh drawing")

        if barh1.data['y'] != [1, 2, 4, 6]:
            return wrong(f"Wrong 'y' value {barh1.data['y']}. Expected [1, 2, 4, 6]")

        if barh1.data['width'] != 100:
            return wrong(f"Wrong 'width' value {barh1.data['height']}. Expected 100")

        barh2 = self.all_figures[11]
        if barh2.type != 'barh':
            return wrong(f'Wrong drawing type {barh2.type}. Expected barh')

        if 'y' not in barh2.data or 'width' not in barh2.data or 'kwargs' not in barh2.data:
            return wrong(f"Expected 'y', 'width', 'kwargs' keys in the data dict of the barh drawing")

        if barh2.data['y'] != [1, 2, 4, 7]:
            return wrong(f"Wrong 'y' value {barh1.data['y']}. Expected [1, 2, 4, 7]")

        if barh2.data['width'] != 200:
            return wrong(f"Wrong 'width' value {barh2.data['height']}. Expected 200")

        # violinplot

        violinplot1 = self.all_figures[12]
        if violinplot1.type != 'violin':
            return wrong(f'Wrong drawing type {violinplot1.type}. Expected violin')

        if 'dataset' not in violinplot1.data or 'kwargs' not in violinplot1.data:
            return wrong(f"Expected 'dataset', 'kwargs' keys in the data dict of the violin drawing")

        if violinplot1.data['dataset'] != [1, 2, 4]:
            return wrong(f"Wrong 'dataset' value {violinplot1.data['dataset']}. Expected [1, 2, 4]")

        violinplot2 = self.all_figures[13]
        if violinplot2.type != 'violin':
            return wrong(f'Wrong drawing type {violinplot2.type}. Expected violin')

        if 'dataset' not in violinplot2.data or 'kwargs' not in violinplot2.data:
            return wrong(f"Expected 'dataset', 'kwargs' keys in the data dict of the violin drawing")

        if violinplot2.data['dataset'] != [1, 2, 5]:
            return wrong(f"Wrong 'dataset' value {violinplot2.data['dataset']}. Expected [1, 2, 5]")

        # imshow

        smile = [[0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
                 [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
                 [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                 [1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
                 [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                 [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
                 [1, 0, 0, 1, 1, 1, 1, 0, 0, 1],
                 [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 1, 1, 1, 1, 1, 1, 0, 0]]

        imshow1 = self.all_figures[14]
        if imshow1.type != 'heatmap':
            return wrong(f'Wrong drawing type {imshow1.type}. Expected heatmap')

        if 'x' not in imshow1.data or 'kwargs' not in imshow1.data:
            return wrong(f"Expected 'x', 'kwargs' keys in the data dict of the heatmap drawing")

        if imshow1.data['x'] != smile:
            return wrong(f"Wrong 'x' value {imshow1.data['x']}. Expected {smile}")

        imshow2 = self.all_figures[15]
        if imshow2.type != 'heatmap':
            return wrong(f'Wrong drawing type {imshow2.type}. Expected heatmap')

        if 'x' not in imshow2.data or 'kwargs' not in imshow2.data:
            return wrong(f"Expected 'x', 'kwargs' keys in the data dict of the heatmap drawing")

        if imshow2.data['x'] != smile:
            return wrong(f"Wrong 'x' value {imshow2.data['x']}. Expected {smile}")

        # boxplot

        boxplot1 = self.all_figures[16]
        if boxplot1.type != 'boxplot':
            return wrong(f'Wrong drawing type {boxplot1.type}. Expected boxplot')

        if 'x' not in boxplot1.data or 'kwargs' not in boxplot1.data:
            return wrong(f"Expected 'x', 'kwargs' keys in the data dict of the boxplot drawing")

        if boxplot1.data['x'] != [1, 2, 4]:
            return wrong(f"Wrong 'x' value {boxplot1.data['x']}. Expected [1, 2, 4]")

        boxplot2 = self.all_figures[17]
        if boxplot2.type != 'boxplot':
            return wrong(f'Wrong drawing type {boxplot2.type}. Expected boxplot')

        if 'x' not in boxplot2.data or 'kwargs' not in boxplot2.data:
            return wrong(f"Expected 'x', 'kwargs' keys in the data dict of the boxplot drawing")

        if boxplot2.data['x'] != [1, 2, 5]:
            return wrong(f"Wrong 'x' value {boxplot2.data['x']}. Expected [1, 2, 5]")

        return correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestMatplotlib('main').run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
