from .drawing import Drawing
from pandas.core.accessor import CachedAccessor
from .matplotlib_handler import MatplotlibHandler


class PandasHandler:
    _saved = False
    _replaced = False

    _PlotAccessor = None
    _Series_plot = None
    _Dataframe_plot = None
    _Dataframe_boxplot = None
    _Dataframe_hist = None
    _Series_hist = None

    @staticmethod
    def replace_plots(drawings):
        try:
            import pandas.plotting as pd
        except ModuleNotFoundError:
            return

        import pandas.plotting

        class CustomPlotAccessor(pandas.plotting.PlotAccessor):
            def __call__(self, *args, **kwargs):
                from pandas.plotting._core import _get_plot_backend

                plot_backend = _get_plot_backend(kwargs.pop("backend", None))

                x, y, kind, kwargs = self._get_call_args(
                    plot_backend.__name__, self._parent, args, kwargs
                )

                if kind not in self._all_kinds:
                    raise ValueError(f"{kind} is not a valid plot kind")

                data = self._parent.copy()

                drawing = Drawing(
                    'pandas',
                    kind,
                    {
                        'data': data,
                        'x': x,
                        'y': y
                    }
                )
                drawings.append(drawing)

        if not PandasHandler._saved:
            PandasHandler._Series_plot = pandas.Series.plot
            PandasHandler._Dataframe_plot = pandas.DataFrame.plot

        pandas.Series.plot = CachedAccessor("plot", CustomPlotAccessor)
        pandas.DataFrame.plot = CachedAccessor("plot", CustomPlotAccessor)

        import pandas.plotting._core

        def boxplot(
            self,
            column=None,
            **kwargs
        ):
            data = self
            drawing = Drawing(
                'pandas',
                'boxplot',
                data={
                    'data': data,
                    'column': column,
                    'kwargs': kwargs
                }
            )
            drawings.append(drawing)

        def hist(
            self,
            column=None,
            **kwargs
        ):
            data = self
            drawing = Drawing(
                'pandas',
                'hist',
                data={
                    'data': data,
                    'column': column,
                    'kwargs': kwargs
                }
            )
            drawings.append(drawing)

        def hist_series(
            self,
            **kwargs
        ):
            data = self
            drawing = Drawing(
                'pandas',
                'hist',
                data={
                    'data': data,
                    'kwargs': kwargs
                }
            )
            drawings.append(drawing)

        if not PandasHandler._saved:
            PandasHandler._saved = True
            PandasHandler._Dataframe_boxplot = pandas.DataFrame.boxplot
            PandasHandler._Dataframe_hist = pandas.DataFrame.hist
            PandasHandler._Series_hist = pandas.Series.hist

        pandas.DataFrame.boxplot = boxplot
        pandas.DataFrame.hist = hist
        pandas.Series.hist = hist_series

        PandasHandler._replaced = True

    @staticmethod
    def revert_plots():
        pass
