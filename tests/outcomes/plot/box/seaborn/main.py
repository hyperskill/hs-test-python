def plot():
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        import seaborn as sns
    except ModuleNotFoundError:
        return

    tips = sns.load_dataset("tips")
    ax = sns.boxplot(x=tips["total_bill"])

    plt.show()


plot()
