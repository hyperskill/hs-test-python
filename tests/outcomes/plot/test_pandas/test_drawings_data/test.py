import unittest

from hstest.check_result import correct, wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest import TestedProgram


class TestSeaborn(PlottingTest):
    @dynamic_test
    def test(self):

        import matplotlib
        import pandas as pd

        program = TestedProgram()
        program.start()

        if len(self.all_figures) != 22:
            return wrong(f'Expected 22 plots to be plotted using matplotlib library, found {len(self.all_figures)}')

        # area

        area1 = self.all_figures[0]
        if area1.type != 'area':
            return wrong(f'Wrong drawing type {area1.type}. Expected area')

        if 'data' not in area1.data or 'x' not in area1.data or 'y' not in area1.data:
            return wrong(f"Expected 'data', 'x', 'y' key in the data dict of the area drawing")

        if type(area1.data['data']) != pd.DataFrame:
            return wrong(f"Wrong 'data' type {type(area1.data['data'])}. Expected {pd.DataFrame}")

        area2 = self.all_figures[1]
        if area2.type != 'area':
            return wrong(f'Wrong drawing type {area2.type}. Expected area')

        if 'data' not in area2.data or 'x' not in area2.data or 'y' not in area2.data:
            return wrong(f"Expected 'data', 'x', 'y' key in the data dict of the area drawing")

        if type(area2.data['data']) != pd.DataFrame:
            return wrong(f"Wrong 'data' type {type(area2.data['data'])}. Expected {pd.DataFrame}")

        # bar

        bar1 = self.all_figures[2]
        if bar1.type != 'bar':
            return wrong(f'Wrong drawing type {bar1.type}. Expected bar')

        if 'data' not in bar1.data or 'x' not in bar1.data or 'y' not in bar1.data:
            return wrong(f"Expected 'data', 'x', 'y' key in the data dict of the bar drawing")

        if type(bar1.data['data']) != pd.DataFrame:
            return wrong(f"Wrong 'data' type {type(bar1.data['data'])}. Expected {pd.DataFrame}")

        if bar1.data['x'] != 'lab':
            return wrong(f"Wrong 'x' value {bar1.data['x']}. Expected 'lab'")

        if bar1.data['y'] != 'val':
            return wrong(f"Wrong 'y' value {bar1.data['y']}. Expected 'val'")

        for drawing in self.all_figures:
            if drawing.library != 'pandas':
                return wrong('Drawings plotted using wrong library!')

        bar2 = self.all_figures[3]
        if bar2.type != 'bar':
            return wrong(f'Wrong drawing type {bar2.type}. Expected bar')

        if 'data' not in bar2.data or 'x' not in bar2.data or 'y' not in bar2.data:
            return wrong(f"Expected 'data', 'x', 'y' key in the data dict of the bar drawing")

        if type(bar2.data['data']) != pd.DataFrame:
            return wrong(f"Wrong 'data' type {type(bar2.data['data'])}. Expected {pd.DataFrame}")

        if bar2.data['x'] != 'lab':
            return wrong(f"Wrong 'x' value {bar2.data['x']}. Expected 'lab'")

        if bar2.data['y'] != 'val':
            return wrong(f"Wrong 'y' value {bar2.data['y']}. Expected 'val'")

        # barh

        barh1 = self.all_figures[4]
        if barh1.type != 'barh':
            return wrong(f'Wrong drawing type {barh1.type}. Expected barh')

        if 'data' not in barh1.data or 'x' not in barh1.data or 'y' not in barh1.data:
            return wrong(f"Expected 'data', 'x', 'y' key in the data dict of the barh drawing")

        if type(barh1.data['data']) != pd.DataFrame:
            return wrong(f"Wrong 'data' type {type(barh1.data['data'])}. Expected {pd.DataFrame}")

        if barh1.data['x'] != 'lab':
            return wrong(f"Wrong 'x' value {barh1.data['x']}. Expected 'lab'")

        if barh1.data['y'] != 'val':
            return wrong(f"Wrong 'y' value {barh1.data['y']}. Expected 'val'")

        barh2 = self.all_figures[5]
        if barh2.type != 'barh':
            return wrong(f'Wrong drawing type {barh2.type}. Expected barh')

        if 'data' not in barh2.data or 'x' not in barh2.data or 'y' not in barh2.data:
            return wrong(f"Expected 'data', 'x', 'y' key in the data dict of the barh drawing")

        if type(barh2.data['data']) != pd.DataFrame:
            return wrong(f"Wrong 'data' type {type(barh2.data['data'])}. Expected {pd.DataFrame}")

        if barh2.data['x'] != 'lab':
            return wrong(f"Wrong 'x' value {barh2.data['x']}. Expected 'lab'")

        if barh2.data['y'] != 'val':
            return wrong(f"Wrong 'y' value {barh2.data['y']}. Expected 'val'")

        # box

        for box in (self.all_figures[6], self.all_figures[7]):
            if box.type != 'box':
                return wrong(f'Wrong drawing type {box.type}. Expected box')

            if 'data' not in box.data or 'x' not in box.data or 'y' not in box.data:
                return wrong(f"Expected 'data', 'x', 'y' key in the data dict of the box drawing")

            if type(box.data['data']) != pd.DataFrame:
                return wrong(f"Wrong 'data' type {type(box.data['data'])}. Expected {pd.DataFrame}")

        # kde

        for kde in (self.all_figures[8], self.all_figures[9]):
            if kde.type != 'kde':
                return wrong(f'Wrong drawing type {kde.type}. Expected kde')

            if 'data' not in kde.data or 'x' not in kde.data or 'y' not in kde.data:
                return wrong(f"Expected 'data', 'x', 'y' key in the data dict of the kde drawing")

            if type(kde.data['data']) != pd.Series:
                return wrong(f"Wrong 'data' type {type(kde.data['data'])}. Expected {pd.Series}")

        # hexbin

        for hexbin in (self.all_figures[10], self.all_figures[11]):
            if hexbin.type != 'hexbin':
                return wrong(f'Wrong drawing type {hexbin.type}. Expected hexbin')

            if 'data' not in hexbin.data or 'x' not in hexbin.data or 'y' not in hexbin.data:
                return wrong(f"Expected 'data', 'x', 'y' key in the data dict of the hexbin drawing")

            if type(hexbin.data['data']) != pd.DataFrame:
                return wrong(f"Wrong 'data' type {type(hexbin.data['data'])}. Expected {pd.DataFrame}")

            if hexbin.data['x'] != 'x':
                return wrong(f"Wrong 'x' value {hexbin.data['x']}. Expected 'x'")

            if hexbin.data['y'] != 'y':
                return wrong(f"Wrong 'y' value {hexbin.data['y']}. Expected 'y'")

        # hist

        for hist in (self.all_figures[12], self.all_figures[13]):
            if hist.type != 'hist':
                return wrong(f'Wrong drawing type {hist.type}. Expected hist')

            if 'data' not in hist.data or 'x' not in hist.data or 'y' not in hist.data or 'kwargs' not in hist.data:
                return wrong(f"Expected 'data', 'x', 'y' key in the data dict of the hist drawing")

            if type(hist.data['data']) != pd.DataFrame:
                return wrong(f"Wrong 'data' type {type(hist.data['data'])}. Expected {pd.DataFrame}")

            if 'bins' not in hist.data['kwargs'] or hist.data['kwargs']['bins'] != 12:
                return wrong(f"Wrong 'bins' value. Expected 12")

            if 'alpha' not in hist.data['kwargs'] or hist.data['kwargs']['alpha'] != 0.5:
                return wrong(f"Wrong 'bins' value. Expected 0,5")

        # line

        for line in (self.all_figures[14], self.all_figures[15]):
            if line.type != 'line':
                return wrong(f'Wrong drawing type {line.type}. Expected line')

            if 'data' not in hist.data or 'x' not in hist.data or 'y' not in hist.data or 'kwargs' not in hist.data:
                return wrong(f"Expected 'data', 'x', 'y' key in the data dict of the line drawing")

            if type(hist.data['data']) != pd.DataFrame:
                return wrong(f"Wrong 'data' type {type(hist.data['data'])}. Expected {pd.DataFrame}")

        # pie

        for pie in (self.all_figures[16], self.all_figures[17]):
            if pie.type != 'pie':
                return wrong(f'Wrong drawing type {pie.type}. Expected pie')

            if 'data' not in pie.data or 'x' not in pie.data or 'y' not in pie.data or 'kwargs' not in pie.data:
                return wrong(f"Expected 'data', 'x', 'y' key in the data dict of the pie drawing")

            if type(pie.data['data']) != pd.DataFrame:
                return wrong(f"Wrong 'data' type {type(pie.data['data'])}. Expected {pd.DataFrame}")

            if pie.data['y'] != 'mass':
                return wrong(f"Wrong 'y' value {pie.data['y']}. Expected 'mass'")

        # scatter

        for scatter in (self.all_figures[18], self.all_figures[19]):
            if scatter.type != 'scatter':
                return wrong(f'Wrong drawing type {pie.type}. Expected scatter')

            if 'data' not in scatter.data or 'x' not in scatter.data or 'y' not in scatter.data or 'kwargs' not in scatter.data:
                return wrong(f"Expected 'data', 'x', 'y' key in the data dict of the scatter drawing")

            if type(scatter.data['data']) != pd.DataFrame:
                return wrong(f"Wrong 'data' type {type(scatter.data['data'])}. Expected {pd.DataFrame}")

            if scatter.data['x'] != 'length':
                return wrong(f"Wrong 'y' value {scatter.data['x']}. Expected 'length'")

            if scatter.data['y'] != 'width':
                return wrong(f"Wrong 'y' value {scatter.data['y']}. Expected 'width'")

        # hist from df and series

        hist1 = self.all_figures[20]
        if hist1.type != 'hist':
            return wrong(f'Wrong drawing type {hist1.type}. Expected hist')

        if 'data' not in hist1.data or 'column' not in hist1.data or 'kwargs' not in hist1.data:
            return wrong(f"Expected 'data', 'x', 'y' key in the data dict of the hist drawing")

        if type(hist1.data['data']) != pd.DataFrame:
            return wrong(f"Wrong 'data' type {type(hist1.data['data'])}. Expected {pd.DataFrame}")

        if hist1.data['column'] != ['Col1', 'Col2', 'Col3']:
            return wrong(f"Wrong 'column' value {hist1.data['column']}. Expected ['Col1', 'Col2', 'Col3']")

        hist2 = self.all_figures[21]
        if hist2.type != 'hist':
            return wrong(f'Wrong drawing type {hist2.type}. Expected hist')

        if 'data' not in hist1.data or 'kwargs' not in hist1.data:
            return wrong(f"Expected 'data', 'kwargs' key in the data dict of the hist drawing")

        if type(hist2.data['data']) != pd.Series:
            return wrong(f"Wrong 'data' type {type(hist2.data['data'])}. Expected {pd.Series}")

        for drawing in self.all_figures:
            if drawing.library != 'pandas':
                return wrong('Drawings plotted using wrong library!')

        return correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestSeaborn('main').run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
