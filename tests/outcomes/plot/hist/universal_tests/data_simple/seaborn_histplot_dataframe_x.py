def plot():
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        import pandas as pd
        import numpy as np
    except ModuleNotFoundError:
        return

    df = pd.DataFrame(np.array([[1, 2], [2, 3], [3, 4], [4, 5], [5, 6]]),
                      columns=['one', 'two'])

    sns.histplot(df, x='one')

    plt.show()


plot()
