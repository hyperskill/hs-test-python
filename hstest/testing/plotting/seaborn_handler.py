import pandas as pd

from hstest.testing.plotting.drawing import Drawing, DrawingType, DrawingLibrary
from importlib import reload
from hstest.testing.plotting.matplotlib_handler import MatplotlibHandler
from pandas.api.types import is_numeric_dtype


class SeabornHandler:
    _saved = False
    _replaced = False

    _displot = None
    _histplot = None
    _lineplot = None
    _lmplot = None
    _scatterplot = None
    _catplot = None
    _barplot = None
    _violinplot = None
    _heatmap = None
    _boxplot = None

    @staticmethod
    def replace_plots(drawings):
        try:
            import seaborn as sns
            import numpy as np
        except ModuleNotFoundError:
            return

        def displot(data=None, **kwargs):
            x = None if 'x' not in kwargs else kwargs['x']
            y = None if 'y' not in kwargs else kwargs['y']

            if data is None:
                drawing = Drawing(
                    DrawingLibrary.seaborn,
                    DrawingType.dis,
                    {
                        'x': np.array(x),
                        'y': np.array(y)
                    }
                )
                drawings.append(drawing)
                return

            x_arr = []
            y_arr = []

            if not x and not y:
                for column in data.columns:
                    if not is_numeric_dtype(data[column]):
                        continue
                    drawing = Drawing(
                        DrawingLibrary.seaborn,
                        DrawingType.dis,
                        {
                            'x': np.array([column]),
                            'y': data[column].to_numpy()
                        }
                    )
                    drawings.append(drawing)
                return

            if x:
                x_arr = data[x].to_numpy()
            if y:
                y_arr = data[y].to_numpy()

            drawing = Drawing(
                DrawingLibrary.seaborn,
                DrawingType.dis,
                {
                    'x': np.array(x_arr),
                    'y': np.array(y_arr)
                }
            )
            drawings.append(drawing)

        def histplot(data=None, **kwargs):
            if data is not None:
                if 'x' in kwargs and kwargs['x'] is not None:
                    drawings.append(
                        Drawing.get_hist_drawing(
                            data[kwargs['x']],
                            DrawingLibrary.seaborn
                        )
                    )
                elif 'y' in kwargs and kwargs['y'] is not None:
                    drawings.append(
                        Drawing.get_hist_drawing(
                            data[kwargs['y']],
                            DrawingLibrary.seaborn
                        )
                    )

        def lineplot(*, data=None, x=None, y=None, **kwargs):
            if x is not None:
                x_array = data[x].to_numpy()
            else:
                x_array = data.index.to_numpy()

            if y is not None:
                y_array = data[y].to_numpy()

                drawing = Drawing(
                    DrawingLibrary.seaborn,
                    DrawingType.line,
                    {
                        'x': x_array,
                        'y': y_array,
                    }
                )
                drawings.append(drawing)
                return drawings

            for column in data.columns:
                if not is_numeric_dtype(data[column]):
                    continue

                drawing = Drawing(
                    DrawingLibrary.pandas,
                    DrawingType.line,
                    {
                        'x': x_array,
                        'y': data[column].to_numpy()
                    }
                )
                drawings.append(drawing)

        def lmplot(x=None, y=None, data=None, **kwargs):
            drawing = Drawing(
                DrawingLibrary.seaborn,
                DrawingType.lm,
                {
                    'data': data,
                    'x': x,
                    'y': y,
                    'kwargs': kwargs
                }
            )
            drawings.append(drawing)

        def scatterplot(x=None, y=None, data=None, **kwargs):

            if x is not None and y is not None:
                drawing = Drawing(
                    DrawingLibrary.seaborn,
                    DrawingType.scatter,
                    {
                        'x': data[x].to_numpy(),
                        'y': data[y].to_numpy(),
                    }
                )
                drawings.append(drawing)
                return

            if x is not None:
                x_arr = data[x]
                drawing = Drawing(
                    DrawingLibrary.seaborn,
                    DrawingType.scatter,
                    {
                        'x': x_arr.to_numpy(),
                        'y': np.array([]),
                    }
                )
                drawings.append(drawing)
                return

            if y is not None:
                y_arr = data[y]
                drawing = Drawing(
                    DrawingLibrary.seaborn,
                    DrawingType.scatter,
                    {
                        'x': np.array([]),
                        'y': y_arr.to_numpy(),
                    }
                )
                drawings.append(drawing)
                return

            x = data.index

            for column in data.columns:
                if not is_numeric_dtype(data[column]):
                    continue

                drawing = Drawing(
                    DrawingLibrary.seaborn,
                    DrawingType.scatter,
                    {
                        'x': x.to_numpy(),
                        'y': data[column].to_numpy(),
                    }
                )
                drawings.append(drawing)

        def catplot(x=None, y=None, data=None, **kwargs):
            drawing = Drawing(
                DrawingLibrary.seaborn,
                DrawingType.cat,
                {
                    'data': data,
                    'x': x,
                    'y': y,
                    'kwargs': kwargs
                }
            )
            drawings.append(drawing)

        def barplot(x=None, y=None, data=None, **kwargs):

            x_arr = np.array([])
            y_arr = np.array([])

            if data is not None:
                if x:
                    x_arr = data[x].to_numpy()
                if y:
                    y_arr = data[y].to_numpy()

            drawing = Drawing(
                DrawingLibrary.seaborn,
                DrawingType.bar,
                {
                    'x': x_arr,
                    'y': y_arr
                }
            )
            drawings.append(drawing)

        def violinplot(x=None, y=None, data=None, **kwargs):

            x_arr = np.array([])
            y_arr = np.array([])

            if x:
                x_arr = data[x].to_numpy()
            if y:
                y_arr = data[y].to_numpy()

            if x or y:
                drawing = Drawing(
                    DrawingLibrary.seaborn,
                    DrawingType.violin,
                    {
                        'x': x_arr,
                        'y': y_arr
                    }
                )
                drawings.append(drawing)
                return

            for column in data.columns:
                if not is_numeric_dtype(data[column]):
                    continue
                drawing = Drawing(
                    DrawingLibrary.seaborn,
                    DrawingType.violin,
                    {
                        'x': np.array([column]),
                        'y': data[column].to_numpy()
                    }
                )
                drawings.append(drawing)

        def heatmap(data=None, **kwargs):
            if data is None:
                return

            drawing = Drawing(
                DrawingLibrary.seaborn,
                DrawingType.heatmap,
                {
                    'x': np.array(data)
                }
            )
            drawings.append(drawing)

        def boxplot(x=None, y=None, data=None, **kwargs):

            if data is None:
                drawing = Drawing(
                    DrawingLibrary.seaborn,
                    DrawingType.box,
                    {
                        'x': np.array(x),
                        'y': np.array(y)
                    }
                )
                drawings.append(drawing)
                return

            x_arr = []
            y_arr = []

            if not x and not y:
                for column in data.columns:
                    if not is_numeric_dtype(data[column]):
                        continue
                    drawing = Drawing(
                        DrawingLibrary.seaborn,
                        DrawingType.box,
                        {
                            'x': np.array([column]),
                            'y': data[column].to_numpy()
                        }
                    )
                    drawings.append(drawing)
                return

            if x:
                x_arr = data[x].to_numpy()
            if y:
                y_arr = data[y].to_numpy()

            drawing = Drawing(
                DrawingLibrary.seaborn,
                DrawingType.box,
                {
                    'x': np.array(x_arr),
                    'y': np.array(y_arr)
                }
            )
            drawings.append(drawing)

        if not SeabornHandler._saved:
            SeabornHandler._saved = True
            SeabornHandler._displot = sns.displot
            SeabornHandler._histplot = sns.histplot
            SeabornHandler._lineplot = sns.lineplot
            SeabornHandler._lmplot = sns.lmplot
            SeabornHandler._scatterplot = sns.scatterplot
            SeabornHandler._catplot = sns.catplot
            SeabornHandler._barplot = sns.barplot
            SeabornHandler._violinplot = sns.violinplot
            SeabornHandler._heatmap = sns.heatmap
            SeabornHandler._boxplot = sns.boxplot

        sns.displot = displot
        sns.histplot = histplot
        sns.lineplot = lineplot
        sns.lmplot = lmplot
        sns.scatterplot = scatterplot
        sns.catplot = catplot
        sns.barplot = barplot
        sns.violinplot = violinplot
        sns.heatmap = heatmap
        sns.boxplot = boxplot

        SeabornHandler._replaced = True

    @staticmethod
    def revert_plots():

        if not SeabornHandler._replaced:
            return

        MatplotlibHandler.revert_plots()

        import seaborn as sns

        sns.displot = SeabornHandler._displot
        sns.histplot = SeabornHandler._histplot
        sns.lineplot = SeabornHandler._lineplot
        sns.lmplot = SeabornHandler._lmplot
        sns.scatterplot = SeabornHandler._scatterplot
        sns.catplot = SeabornHandler._catplot
        sns.barplot = SeabornHandler._barplot
        sns.violinplot = SeabornHandler._violinplot
        sns.heatmap = SeabornHandler._heatmap
        sns.boxplot = SeabornHandler._boxplot

        reload(sns)

        SeabornHandler._replaced = False
