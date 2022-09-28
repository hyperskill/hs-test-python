from copy import deepcopy
from importlib import reload
from typing import TYPE_CHECKING

from hstest.testing.plotting.drawing.drawing_data import DrawingData

try:
    import pandas as pd
except ImportError:
    pass

from hstest.testing.plotting.drawing.drawing import Drawing
from hstest.testing.plotting.drawing.drawing_builder import DrawingBuilder
from hstest.testing.plotting.drawing.drawing_library import DrawingLibrary
from hstest.testing.plotting.drawing.drawing_type import DrawingType

if TYPE_CHECKING:
    from hstest.testing.runner.plot_testing_runner import DrawingsStorage


class MatplotlibHandler:
    _saved = False
    _replaced = False

    _Axes = None
    _hist = None
    _plot = None
    _scatter = None
    _pie = None
    _bar = None
    _barh = None
    _violinplot = None
    _imshow = None
    _boxplot = None
    _show = None
    _backend = None
    _matplotlib = None

    @staticmethod
    def replace_plots(drawings: 'DrawingsStorage'):

        try:
            import matplotlib
            import numpy as np
        except ModuleNotFoundError:
            return

        def custom_show_func(*args, **kwargs):
            pass

        def hist(x, *args, data=None, **kw):
            if data is not None:
                try:
                    x = data[x]
                except:
                    pass

            try:
                if type(x) == pd.DataFrame:
                    for col in x.columns:
                        hist(x[col], *args, **kw)
                    return
                elif type(x) == pd.Series:
                    return hist(x.to_numpy(), *args, **kw)
            except:
                pass

            if type(x) != np.ndarray:
                x = np.array(x, dtype=object)
                if len(x.shape) == 2:
                    import matplotlib.cbook as cbook
                    x = np.array(cbook._reshape_2D(x, 'x'), dtype=object)

            if len(x.shape) == 2:
                for i in range(x.shape[1]):
                    hist(x[:, i], *args, **kw)
                return

            drawings.append(
                Drawing(
                    DrawingLibrary.matplotlib,
                    DrawingType.hist,
                    DrawingData(x, np.array([1] * len(x))),
                    kw
                )
            )

        def bar(x, height, *args, data=None, **kw):
            if data is not None:
                try:
                    x = data[x]
                except:
                    pass
                try:
                    height = data[height]
                except:
                    pass

            try:
                if type(x) == pd.DataFrame:
                    for col in x.columns:
                        bar(x[col], *args, **kw)
                    return
                elif type(x) == pd.Series:
                    return bar(x.to_numpy(), height, *args, **kw)
                elif type(height) == pd.Series:
                    return bar(x, height.to_numpy(), *args, **kw)
            except:
                pass

            if type(height) in [int, float]:
                height = np.full((len(x),), height)

            drawings.append(
                Drawing(
                    DrawingLibrary.matplotlib,
                    DrawingType.bar,
                    DrawingData(x, height),
                    kw
                )
            )

        def barh(x, width, *args, data=None, **kw):
            return bar(x, width, *args, data=data, **kw)

        def plot(*args, **kwargs):
            x = list()
            y = list()

            if len(args) > 0:
                if type(args[0]) is list:
                    x = args[0]
            if len(args) > 1:
                if type(args[1]) is list:
                    y = args[1]
            else:
                y = [_ for _ in range(len(x))]

            drawings.append(
                DrawingBuilder.get_line_drawing(
                    x, y,
                    DrawingLibrary.matplotlib,
                    kwargs,
                )
            )

        def scatter(x, y, *a, **kwargs):
            drawings.append(
                DrawingBuilder.get_scatter_drawing(
                    x, y,
                    DrawingLibrary.matplotlib,
                    kwargs,
                )
            )

        def pie(x, *a, **kw):
            # Normalize with other plot libraries
            y = x

            x_arr = [''] * len(y)

            if 'labels' in kw and kw['labels'] is not None:
                x_arr = kw['labels']

            drawing = DrawingBuilder.get_pie_drawing(
                x_arr, y,
                DrawingLibrary.matplotlib,
                kw,
            )
            drawings.append(drawing)

        def violinplot(dataset, *, data=None, **kwargs):
            if data is not None:
                try:
                    dataset = data[dataset]
                except:
                    pass

            drawing = Drawing(
                DrawingLibrary.matplotlib,
                DrawingType.violin,
                dataset,
                kwargs
            )

            drawings.append(drawing)

        def imshow(x, **kwargs):
            curr_data = {
                'x': np.array(x)
            }

            drawing = Drawing(
                DrawingLibrary.matplotlib,
                DrawingType.heatmap,
                None,
                kwargs,
            )
            drawings.append(drawing)

        def boxplot(x, **kwargs):
            curr_data = {
                'x': np.array([None]),
                'y': np.array(x)
            }

            drawing = Drawing(
                DrawingLibrary.matplotlib,
                DrawingType.box,
                None,
                kwargs,
            )
            drawings.append(drawing)

        import matplotlib.axes

        class CustomMatplotlibAxes(matplotlib.axes.Axes):

            def hist(self, x, *a, **kw):
                hist(x, *a, **kw)

            def bar(self, x, height, *a, **kw):
                bar(x, height, *a, **kw)

            def barh(self, y, width, *a, **kw):
                barh(y, width, *a, **kw)

            def plot(self, *args, **kwargs):
                plot(*args, *kwargs)

            def scatter(self, x, y, *a, **kwargs):
                scatter(x, y, *a, **kwargs)

            def pie(self, x, *a, **kw):
                pie(x, *a, **kw)

            def violinplot(self, dataset, **kwargs):
                violinplot(dataset, **kwargs)

            def imshow(self, x, **kwargs):
                imshow(x, **kwargs)

            def boxplot(self, x, **kwargs):
                boxplot(x, **kwargs)

        import matplotlib

        if not MatplotlibHandler._saved:
            MatplotlibHandler._Axes = deepcopy(matplotlib.axes.Axes)

        # should be replaced before import matplotlib.pyplot as plt
        matplotlib.axes.Axes = CustomMatplotlibAxes

        from matplotlib.projections import projection_registry
        projection_registry.register(matplotlib.axes.Axes)

        import matplotlib.pyplot as plt

        if not MatplotlibHandler._saved:
            MatplotlibHandler._saved = True
            MatplotlibHandler._hist = plt.hist
            MatplotlibHandler._plot = plt.plot
            MatplotlibHandler._scatter = plt.scatter
            MatplotlibHandler._pie = plt.pie
            MatplotlibHandler._bar = plt.bar
            MatplotlibHandler._barh = plt.barh
            MatplotlibHandler._violinplot = plt.violinplot
            MatplotlibHandler._imshow = plt.imshow
            MatplotlibHandler._boxplot = plt.boxplot
            MatplotlibHandler._show = plt.show
            MatplotlibHandler._backend = matplotlib.get_backend()

        plt.hist = hist
        plt.plot = plot
        plt.scatter = scatter
        plt.pie = pie
        plt.bar = bar
        plt.barh = barh
        plt.violinplot = violinplot
        plt.imshow = imshow
        plt.boxplot = boxplot
        plt.show = custom_show_func

        matplotlib.use('Agg')

        MatplotlibHandler._replaced = True

    @staticmethod
    def revert_plots():

        if not MatplotlibHandler._replaced:
            return

        import matplotlib.axes
        import matplotlib.figure
        import matplotlib.pyplot as plt

        matplotlib.axes.Axes = MatplotlibHandler._Axes
        plt.hist = MatplotlibHandler._hist
        plt.plot = MatplotlibHandler._plot
        plt.scatter = MatplotlibHandler._scatter
        plt.pie = MatplotlibHandler._pie
        plt.bar = MatplotlibHandler._bar
        plt.barh = MatplotlibHandler._barh
        plt.violinplot = MatplotlibHandler._violinplot
        plt.imshow = MatplotlibHandler._imshow
        plt.boxplot = MatplotlibHandler._boxplot
        plt.show = MatplotlibHandler._show

        from matplotlib.projections import projection_registry

        projection_registry.register(MatplotlibHandler._Axes)
        matplotlib.use(MatplotlibHandler._backend)

        reload(matplotlib.figure)
        reload(matplotlib.pyplot)

        MatplotlibHandler._replaced = False
