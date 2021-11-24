import numpy as np
from hstest import wrong, correct


def test_hist_drawing(figures, correct_plot_count, correct_data):
    if len(figures) != correct_plot_count:
        return wrong(f'Expected {correct_plot_count} plots to be plotted using pandas library, found {len(figures)}')

    for i, hist in enumerate(figures):
        if hist.type != 'hist':
            return wrong(f'Wrong drawing type {hist.type}. Expected hist')

        if not isinstance(hist.data.data, np.ndarray):
            return wrong("The data value should be a ndarray")

        if not np.array_equal(correct_data[i], hist.data.data):
            return wrong('Wrong data of the hist graph')

    return correct()
