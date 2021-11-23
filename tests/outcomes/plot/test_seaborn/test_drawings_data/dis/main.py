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
    sns.displot(data=df, y='Col1')
    sns.displot(data=df, x='Col2')
    sns.displot(data=df)
    sns.displot(x=df['Col1'], y=df['Col2'])

    plt.show()


plot()
