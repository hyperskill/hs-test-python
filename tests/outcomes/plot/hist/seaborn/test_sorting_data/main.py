def plot():
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        import pandas as pd
        import numpy as np
    except ModuleNotFoundError:
        return

    df = pd.DataFrame(np.array([5, 4, 3, 2, 1, 3]), columns=['one'])

    sns.histplot(
        df, y="one"
    )

    sns.histplot(
        df, x="one"
    )

    plt.show()


plot()
