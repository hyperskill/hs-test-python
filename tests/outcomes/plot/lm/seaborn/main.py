def plot():
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
        import seaborn as sns
    except ModuleNotFoundError:
        return

    tips = sns.load_dataset("tips")
    g = sns.lmplot(x="total_bill", y="tip", data=tips)

    plt.show()


plot()
