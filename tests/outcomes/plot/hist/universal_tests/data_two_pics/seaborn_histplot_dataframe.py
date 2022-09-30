def plot():
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        import pandas as pd
        import numpy as np
    except ModuleNotFoundError:
        return

    df = pd.DataFrame(np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]),
                      columns=['one', 'two'])

    sns.histplot(df, bins=10)

    plt.show()


plot()
