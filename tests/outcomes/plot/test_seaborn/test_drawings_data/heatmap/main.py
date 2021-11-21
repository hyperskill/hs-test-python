def plot():
    try:
        import pandas as pd
        import numpy as np
        import seaborn as sns
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return

    uniform_data = [
        [1, 2, 3],
        [7, 8, 9]
    ]

    df = pd.DataFrame({'A': [1, 7], 'B': [2, 8], 'C': [3, 9]})
    sns.heatmap(uniform_data)
    sns.heatmap(df)

    plt.show()


plot()
