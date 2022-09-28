def plot():
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
        import seaborn as sns
    except ModuleNotFoundError:
        return

    df = pd.DataFrame(np.array([5, 2, 1, 4, 5, 3]), columns=['one'])

    sns.histplot(
        df, y="one"
    )

    plt.show()

    sns.histplot(
        df, x="one"
    )

    plt.show()


plot()
