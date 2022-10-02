import numpy as np
from hstest import wrong, correct


def test_pie_drawing(figures, correct_plot_count, correct_data, library_type):
    if len(figures) != correct_plot_count:
        return wrong(
            f'Expected {correct_plot_count} plots to be plotted using {library_type} library, found {len(figures)}')

    for i, pie in enumerate(figures):
        if pie.type != 'pie':
            return wrong(f'Wrong drawing type {pie.type}. Expected pie')

        if pie.library != library_type:
            return wrong(f'{pie.library} is wrong library type. Expected {library_type}')

        if not isinstance(pie.data.y, np.ndarray):
            return wrong("The data value should be a ndarray")

        if not np.array_equal(correct_data[i][:, 0], pie.data.x):
            return wrong('Wrong x data of the pie graph')

        if not np.array_equal(correct_data[i][:, 1], pie.data.y):
            return wrong('Wrong y data of the pie graph')

    return correct()
