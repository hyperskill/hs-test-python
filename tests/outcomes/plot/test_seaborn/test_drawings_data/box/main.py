def plot():
    try:
        import pandas as pd
        import numpy as np
        import seaborn as sns
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return

    df = pd.DataFrame([[1, 2], [3, 4]],
                      columns=['Col1', 'Col2'])
    ax = sns.boxplot(data=df, y='Col1')
    ax = sns.boxplot(data=df, x='Col2')
    ax = sns.boxplot(data=df)
    ax = sns.boxplot(x=df['Col1'], y=df['Col2'])
    plt.show()


plot()
