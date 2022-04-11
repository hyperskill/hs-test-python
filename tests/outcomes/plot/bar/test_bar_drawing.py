import numpy as np

from hstest import correct, wrong
from hstest.testing.plotting.drawing.drawing_data import DrawingData


def test_bar_drawing(figures, correct_data, library_type):
    correct_plot_count = len(correct_data)

    if len(figures) != correct_plot_count:
        return wrong(
            f'Expected {correct_plot_count} plots to be plotted using {library_type} library, found {len(figures)}')

    for i, bar in enumerate(figures):
        if bar.type != 'bar':
            return wrong(f'Wrong drawing type {bar.type}. Expected bar')

        if bar.library != library_type:
            return wrong(f'{bar.library} is wrong library type. Expected {library_type}')

        if not isinstance(bar.data, DrawingData):
            return wrong("The data value should be a ndarray")

        current_correct = np.array(correct_data[i], dtype=object)

        if not np.array_equal(current_correct[:, 0], bar.data.x):
            return wrong('Wrong x data of the bar graph')

        if not np.array_equal(current_correct[:, 1], bar.data.y):
            return wrong('Wrong y data of the bar graph')

    return correct()
