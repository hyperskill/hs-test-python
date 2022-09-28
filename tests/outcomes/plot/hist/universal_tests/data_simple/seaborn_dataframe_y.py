def plot():
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
        import seaborn as sns
    except ModuleNotFoundError:
        return

    df = pd.DataFrame(np.array([[1, 2], [2, 3], [3, 4], [4, 5], [5, 6]]),
                      columns=['one', 'two'])

    sns.histplot(df, y='one', bins=10)

    plt.show()


plot()
