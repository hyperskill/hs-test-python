def plot():
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        import pandas as pd
        import numpy as np
    except ModuleNotFoundError:
        return

    df = pd.DataFrame({'lab': ['A', 'B', 'C'], 'val': [10, 30, 20], 'val1': [5, 10, 15]})

    sns.barplot(x='lab', y='val', data=df)
    plt.show()

    sns.barplot(y='val', data=df)
    plt.show()

    sns.barplot(x='val', data=df)
    plt.show()


plot()
