def plot():
    try:
        import pandas as pd
        import numpy as np
        import seaborn as sns
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return

    df = pd.DataFrame([[1, 2, 3], [2, 6, 4]],
                      columns=['length', 'width', 'test'])
    sns.scatterplot(data=df, x='length', y='width')
    sns.scatterplot(data=df)
    sns.scatterplot(data=df, x='length')
    sns.scatterplot(data=df, y='length')
    plt.show()


plot()
