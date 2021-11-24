import numpy as np
from hstest import wrong, correct


def test_scatter_drawing(figures, correct_plot_count, correct_data, library_type):
    if len(figures) != correct_plot_count:
        return wrong(
            f'Expected {correct_plot_count} plots to be plotted using {library_type} library, found {len(figures)}')

    for i, scatter in enumerate(figures):
        if scatter.type != 'scatter':
            return wrong(f'Wrong drawing type {scatter.type}. Expected scatter')

        if scatter.library != library_type:
            return wrong(f'{scatter.library} is wrong library type. Expected {library_type}')

        if not isinstance(scatter.data.data, np.ndarray):
            return wrong("The data value should be a ndarray")

        if not np.array_equal(correct_data[i], scatter.data.data):
            return wrong('Wrong data of the scatter graph')

    return correct()
