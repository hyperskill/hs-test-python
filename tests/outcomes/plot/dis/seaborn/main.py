def plot():
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        import seaborn as sns
    except ModuleNotFoundError:
        return

    penguins = sns.load_dataset("penguins")
    sns.displot(data=penguins, x="flipper_length_mm")

    plt.show()


plot()
