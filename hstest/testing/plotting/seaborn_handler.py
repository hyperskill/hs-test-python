from .drawing import Drawing


class SeabornHandler:

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

    @staticmethod
    def revert_plots():
        pass
