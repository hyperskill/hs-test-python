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
    sns.violinplot(data=df, y='width', palette="Set3", bw=.2, cut=1, linewidth=1)
    sns.violinplot(data=df, x='width', palette="Set3", bw=.2, cut=1, linewidth=1)
    sns.violinplot(data=df, palette="Set3", bw=.2, cut=1, linewidth=1)
    plt.show()


plot()
