from hstest import StageTest


class MatplotlibTest(StageTest):
    def __init__(self, source: str = ''):
        super().__init__(source)

        self._all_figures = []
        self._new_figures = []

        import matplotlib
        import matplotlib.pyplot as plt
        from matplotlib._pylab_helpers import Gcf
        matplotlib.use("agg")

        def custom_show_func(*args, **kwargs):
            managers = Gcf.get_all_fig_managers()
            for m in managers:
                self._all_figures.append(m.canvas.figure)
                self._new_figures.append(m.canvas.figure)
                Gcf.destroy(m.num)

        plt.show = custom_show_func

    @property
    def new_figures(self):
        result = self._new_figures
        self._new_figures = []
        return result

    @property
    def all_figures(self):
        return self._all_figures
