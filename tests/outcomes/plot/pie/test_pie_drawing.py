import numpy as np

from hstest import correct, wrong


def test_pie_drawing(figures, correct_plot_count, correct_data, library_type):
    if len(figures) != correct_plot_count:
        return wrong(
            f'Expected {correct_plot_count} plots to be plotted '
            f'using {library_type} library, found {len(figures)}'
        )

    for i, pie in enumerate(figures):
        if pie.type != 'pie':
            return wrong(f'Wrong drawing type {pie.type}. Expected pie')

        if pie.library != library_type:
            return wrong(f'{pie.library} is wrong library type. Expected {library_type}')

        if not isinstance(pie.data, np.ndarray):
            return wrong("The data value should be a ndarray")

        if not np.array_equal(correct_data[i], pie.data.data):
            return wrong('Wrong data of the pie graph')

    return correct()
