def plot():
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
    except ModuleNotFoundError:
        return

    fig, ax = plt.subplots()

    df = pd.DataFrame(np.array([1, 2, 3, 4, 5]), columns=["one"])

    ax.bar(df.one, height=np.array([2, 3, 4, 5, 6]))
    plt.show()


plot()
