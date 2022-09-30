def plot():
    try:
        import pandas as pd
        import numpy as np
        import seaborn as sns
    except ModuleNotFoundError:
        return

    df = pd.DataFrame({
        'a': [1, 3, 2],
        'b': [1, 3, 2]
    }, index=[2, 4, 6])
    sns.lineplot(data=df, x="a", y="b")
    sns.lineplot(data=df)

    import matplotlib.pyplot as plt

    plt.show()


plot()
