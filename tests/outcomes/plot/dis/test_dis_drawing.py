from hstest import correct, wrong


def test_dis_drawing(figures, correct_plot_count, library_type):
    if len(figures) != correct_plot_count:
        return wrong(
            f'Expected {correct_plot_count} plots to be plotted '
            f'using {library_type} library, found {len(figures)}'
        )

    for i, dis in enumerate(figures):
        if dis.type != 'dis':
            return wrong(f'Wrong drawing type {dis.type}. Expected dis')

        if dis.library != library_type:
            return wrong(f'{dis.library} is wrong library type. Expected {library_type}')

        if dis.data is not None:
            return wrong("The data value should be None")

    return correct()
