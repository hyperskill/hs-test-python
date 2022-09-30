def plot():
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        import pandas as pd
        import numpy as np
    except ModuleNotFoundError:
        return

    exercise = sns.load_dataset("exercise")
    g = sns.catplot(x="time", y="pulse", hue="kind", data=exercise)

    plt.show()


plot()
