from hstest import correct, wrong


def test_cat_drawing(figures, correct_plot_count, library_type):
    if len(figures) != correct_plot_count:
        return wrong(
            f'Expected {correct_plot_count} plots to be plotted '
            f'using {library_type} library, found {len(figures)}'
        )

    for i, cat in enumerate(figures):
        if cat.type != 'cat':
            return wrong(f'Wrong drawing type {cat.type}. Expected cat')

        if cat.library != library_type:
            return wrong(f'{cat.library} is wrong library type. Expected {library_type}')

        if cat.data is not None:
            return wrong("The data value should be None")

    return correct()
