from hstest.testing.plotting.drawing import Drawing, DrawingType, DrawingLibrary
from copy import deepcopy
from importlib import reload


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
    def replace_plots(drawings):

        try:
            import matplotlib
        except ModuleNotFoundError:
            return

        def custom_show_func(*args, **kwargs):
            pass

        def hist(x, *a, **kw):
            drawing = Drawing(
                DrawingLibrary.matplotlib,
                DrawingType.hist,
                {
                    'x': x
                }
            )
            drawings.append(drawing)

        def plot(*args, **kwargs):
            drawing = Drawing(
                DrawingLibrary.matplotlib,
                DrawingType.line,
                {
                    'args': args
                }
            )
            drawings.append(drawing)

        def scatter(x, y, *a, **kwargs):
            drawing = Drawing(
                DrawingLibrary.matplotlib,
                DrawingType.scatter,
                {
                    'x': x,
                    'y': y
                }
            )
            drawings.append(drawing)

        def pie(x, *a, **kw):
            drawing = Drawing(
                DrawingLibrary.matplotlib,
                DrawingType.pie,
                {
                    'x': x
                }
            )
            drawings.append(drawing)

        def bar(x, height, width=0.8, bottom=None, **kwargs):
            drawing = Drawing(
                DrawingLibrary.matplotlib,
                DrawingType.bar,
                {
                    'x': x,
                    'height': height,
                    'kwargs': kwargs
                }
            )
            drawings.append(drawing)

        def barh(y, width, height=0.8, left=None, **kwargs):
            drawing = Drawing(
                DrawingLibrary.matplotlib,
                DrawingType.bar,
                {
                    'y': y,
                    'width': width,
                    'kwargs': kwargs
                }
            )
            drawings.append(drawing)

        def violinplot(dataset, **kwargs):
            drawing = Drawing(
                DrawingLibrary.matplotlib,
                DrawingType.violin,
                {
                    'dataset': dataset,
                    'kwargs': kwargs
                }
            )
            drawings.append(drawing)

        def imshow(x, **kwargs):
            drawing = Drawing(
                DrawingLibrary.matplotlib,
                DrawingType.heatmap,
                {
                    'x': x,
                    'kwargs': kwargs
                }
            )
            drawings.append(drawing)

        def boxplot(x, **kwargs):
            drawing = Drawing(
                DrawingLibrary.matplotlib,
                DrawingType.box,
                {
                    'x': x,
                    'kwargs': kwargs
                }
            )
            drawings.append(drawing)

        import matplotlib.axes

        class CustomMatplotlibAxes(matplotlib.axes.Axes):

            def hist(self, x, *a, **kw):
                hist(x, *a, **kw)

            def plot(self, *args, **kwargs):
                plot(*args, *kwargs)

            def scatter(self, x, y, *a, **kwargs):
                scatter(x, y, *a, **kwargs)

            def pie(self, x, *a, **kw):
                pie(x, *a, **kw)

            def bar(self, x, height, width=0.8, bottom=None, **kwargs):
                bar(x, height, width=width, bottom=bottom, **kwargs)

            def barh(self, y, width, height=0.8, left=None, **kwargs):
                barh(y, width, height=height, left=left, **kwargs)

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
