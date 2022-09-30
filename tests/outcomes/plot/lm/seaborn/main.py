def plot():
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        import pandas as pd
        import numpy as np
    except ModuleNotFoundError:
        return

    tips = sns.load_dataset("tips")
    g = sns.lmplot(x="total_bill", y="tip", data=tips)

    plt.show()


plot()
