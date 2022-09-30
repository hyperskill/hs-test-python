def plot():
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        import pandas as pd
        import numpy as np
    except ModuleNotFoundError:
        return

    tips = sns.load_dataset("tips")
    ax = sns.violinplot(x=tips["total_bill"])

    plt.show()


plot()
