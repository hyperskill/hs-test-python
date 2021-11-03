from .drawing import Drawing
from importlib import reload
from hstest.testing.plotting.matplotlib_handler import MatplotlibHandler


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
        except ModuleNotFoundError:
            return

        lib_type = 'seaborn'

        def displot(data=None, **kwargs):
            drawing = Drawing(
                lib_type,
                'displot',
                {
                    'data': data,
                    'kwargs': kwargs
                }
            )
            drawings.append(drawing)

        def histplot(data=None, **kwargs):
            drawing = Drawing(
                lib_type,
                'histplot',
                {
                    'data': data,
                    'kwargs': kwargs
                }
            )
            drawings.append(drawing)

        def lineplot(*, data=None, x=None, y=None, **kwargs):
            drawing = Drawing(
                lib_type,
                'lineplot',
                {
                    'data': data,
                    'x': x,
                    'y': y,
                    'kwargs': kwargs
                }
            )
            drawings.append(drawing)

        def lmplot(x=None, y=None, data=None, **kwargs):
            drawing = Drawing(
                lib_type,
                'lmplot',
                {
                    'data': data,
                    'x': x,
                    'y': y,
                    'kwargs': kwargs
                }
            )
            drawings.append(drawing)

        def scatterplot(x=None, y=None, data=None, **kwargs):
            drawing = Drawing(
                lib_type,
                'scatterplot',
                {
                    'data': data,
                    'x': x,
                    'y': y,
                    'kwargs': kwargs
                }
            )
            drawings.append(drawing)

        def catplot(x=None, y=None, data=None, **kwargs):
            drawing = Drawing(
                lib_type,
                'catplot',
                {
                    'data': data,
                    'x': x,
                    'y': y,
                    'kwargs': kwargs
                }
            )
            drawings.append(drawing)

        def barplot(x=None, y=None, data=None, **kwargs):
            drawing = Drawing(
                lib_type,
                'barplot',
                {
                    'data': data,
                    'x': x,
                    'y': y,
                    'kwargs': kwargs
                }
            )
            drawings.append(drawing)

        def violinplot(x=None, y=None, data=None, **kwargs):
            drawing = Drawing(
                lib_type,
                'violinplot',
                {
                    'data': data,
                    'x': x,
                    'y': y,
                    'kwargs': kwargs
                }
            )
            drawings.append(drawing)

        def heatmap(data=None, **kwargs):
            drawing = Drawing(
                lib_type,
                'heatmap',
                {
                    'data': data,
                    'kwargs': kwargs
                }
            )
            drawings.append(drawing)

        def boxplot(x=None, y=None, data=None, **kwargs):
            drawing = Drawing(
                lib_type,
                'boxplot',
                {
                    'data': data,
                    'x': x,
                    'y': y,
                    'kwargs': kwargs
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
