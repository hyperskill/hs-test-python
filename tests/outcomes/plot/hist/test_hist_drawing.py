import numpy as np

from hstest import correct, wrong


def test_hist_drawing(figures, correct_data, library_type):
    correct_plot_count = len(correct_data)

    if len(figures) != correct_plot_count:
        return wrong(
            f'Expected {correct_plot_count} plots to be plotted using {library_type} library, found {len(figures)}')

    for i, hist in enumerate(figures):
        if hist.type != 'hist':
            return wrong(f'Wrong drawing type {hist.type}. Expected hist')

        if hist.library != library_type:
            return wrong(f'{hist.library} is wrong library type. Expected {library_type}')

        if not isinstance(hist.data, np.ndarray):
            return wrong("The data value should be a ndarray")

        if not correct_data[i] == hist.data.tolist():
            return wrong('Wrong data of the hist graph')

    return correct()
