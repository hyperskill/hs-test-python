from hstest import correct, wrong


def test_lm_drawing(figures, correct_plot_count, library_type):
    if len(figures) != correct_plot_count:
        return wrong(
            f'Expected {correct_plot_count} plots to be plotted '
            f'using {library_type} library, found {len(figures)}'
        )

    for i, lm in enumerate(figures):
        if lm.type != 'lm':
            return wrong(f'Wrong drawing type {lm.type}. Expected lm')

        if lm.library != library_type:
            return wrong(f'{lm.library} is wrong library type. Expected {library_type}')

        if lm.data is not None:
            return wrong("The data value should be None")

    return correct()
