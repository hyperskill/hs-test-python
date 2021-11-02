from .drawing import Drawing


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
    _Axes = None
    _backend = None

    @staticmethod
    def replace_plots(drawings):
        try:
            import matplotlib
        except ModuleNotFoundError:
            return

        lib_type = 'matplotlib'

        def custom_show_func(*args, **kwargs):
            pass

        def hist(x, *a, **kw):
            drawing = Drawing(
                lib_type,
                'hist',
                {
                    'x': x
                }
            )
            drawings.append(drawing)

        def plot(*args, **kwargs):
            drawing = Drawing(
                lib_type,
                'plot',
                {
                    'args': args
                }
            )
            drawings.append(drawing)

        def scatter(x, y, *a, **kwargs):
            drawing = Drawing(
                lib_type,
                'scatter',
                {
                    'x': x,
                    'y': y
                }
            )
            drawings.append(drawing)

        def pie(x, *a, **kw):
            drawing = Drawing(
                lib_type,
                'pie',
                {
                    'x': x
                }
            )
            drawings.append(drawing)

        def bar(x, height, width=0.8, bottom=None, **kwargs):
            drawing = Drawing(
                lib_type,
                'bar',
                {
                    'x': x,
                    'height': height,
                    'kwargs': kwargs
                }
            )
            drawings.append(drawing)

        def barh(y, width, height=0.8, left=None, **kwargs):
            drawing = Drawing(
                lib_type,
                'barh',
                {
                    'y': y,
                    'width': width,
                    'kwargs': kwargs
                }
            )
            drawings.append(drawing)

        def violinplot(dataset, **kwargs):
            drawing = Drawing(
                lib_type,
                'violin',
                {
                    'dataset': dataset,
                    'kwargs': kwargs
                }
            )
            drawings.append(drawing)

        def imshow(x, **kwargs):
            drawing = Drawing(
                lib_type,
                'heatmap',
                {
                    'x': x,
                    'kwargs': kwargs
                }
            )
            drawings.append(drawing)

        def boxplot(x, **kwargs):
            drawing = Drawing(
                lib_type,
                'boxplot',
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

        if not MatplotlibHandler._saved:
            MatplotlibHandler._Axes = matplotlib.axes.Axes

        # should be replaced before import matplotlib.pyplot as plt
        matplotlib.axes.Axes = CustomMatplotlibAxes

        import matplotlib.pyplot as plt

        if not MatplotlibHandler._saved:
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

        if not MatplotlibHandler._saved:
            MatplotlibHandler._saved = True

        matplotlib.use('Agg')

        MatplotlibHandler._replaced = True

    @staticmethod
    def revert_plots():
        pass
