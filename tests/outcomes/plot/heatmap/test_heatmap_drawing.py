from hstest import correct, wrong


def test_heatmap_drawing(figures, correct_plot_count, library_type):
    if len(figures) != correct_plot_count:
        return wrong(
            f'Expected {correct_plot_count} plots to be plotted '
            f'using {library_type} library, found {len(figures)}'
        )

    for i, heatmap in enumerate(figures):
        if heatmap.type != 'heatmap':
            return wrong(f'Wrong drawing type {heatmap.type}. Expected heatmap')

        if heatmap.library != library_type:
            return wrong(f'{heatmap.library} is wrong library type. Expected {library_type}')

        if heatmap.data is not None:
            return wrong("The data value should be None")

    return correct()
