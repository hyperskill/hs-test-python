def plot():
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
    except ModuleNotFoundError:
        return

    df = pd.DataFrame(
        np.array([[1, 2, 3], [2, 3, 4], [3, 4, 5]]),
        columns=["one", "two", "three"],
        index=["Mercury", "Venus", "Earth"],
    )

    df.plot.pie(y="one")

    plt.show()


plot()
