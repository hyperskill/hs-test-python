from hstest import wrong, correct


def test_violin_drawing(figures, correct_plot_count, library_type):
    if len(figures) != correct_plot_count:
        return wrong(
            f'Expected {correct_plot_count} plots to be plotted using {library_type} library, found {len(figures)}')

    for i, violin in enumerate(figures):
        if violin.type != 'violin':
            return wrong(f'Wrong drawing type {violin.type}. Expected violin')

        if violin.library != library_type:
            return wrong(f'{violin.library} is wrong library type. Expected {library_type}')

        if violin.data is not None:
            return wrong("The data value should be None")

    return correct()
