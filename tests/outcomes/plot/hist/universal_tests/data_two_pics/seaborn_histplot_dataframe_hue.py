def plot():
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
        import seaborn as sns
    except ModuleNotFoundError:
        return

    df = pd.DataFrame(
        np.array(
            [
                [1, 1],
                [2, 2],
                [3, 1],
                [4, 2],
                [5, 1],
                [6, 2],
                [7, 1],
                [8, 2],
                [9, 1],
                [10, 2],
            ]
        ),
        columns=["one", "two"],
    )

    sns.histplot(df, x="one", hue="two", bins=10)

    plt.show()


plot()
