import numpy as np
from hstest import wrong, correct


def test_bar_drawing(figures, correct_plot_count, correct_data, library_type):
    if len(figures) != correct_plot_count:
        return wrong(
            f'Expected {correct_plot_count} plots to be plotted using {library_type} library, found {len(figures)}')

    for i, bar in enumerate(figures):
        if bar.type != 'bar':
            return wrong(f'Wrong drawing type {bar.type}. Expected bar')

        if bar.library != library_type:
            return wrong(f'{bar.library} is wrong library type. Expected {library_type}')

        if not isinstance(bar.data.data, np.ndarray):
            return wrong("The data value should be a ndarray")

        print(type(correct_data[i]))
        print(type(bar.data.data))

        if not np.array_equal(correct_data[i], bar.data.data):
            return wrong('Wrong data of the bar graph')

    return correct()
