def plot():
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return

    df = pd.DataFrame(np.array([[1, 1], [2, 2], [3, 1], [4, 2], [5, 1],
                                [6, 2], [7, 1], [8, 2], [9, 1], [10, 2], ]),
                      columns=['one', 'two'])

    df['one'].hist(by=df['two'])

    plt.show()


plot()
