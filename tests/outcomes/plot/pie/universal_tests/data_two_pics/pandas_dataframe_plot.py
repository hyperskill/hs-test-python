def plot():
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
    except ModuleNotFoundError:
        return

    df = pd.DataFrame(
        np.array([[1, 2], [2, 3], [3, 4]]),
        columns=["one", "two"],
        index=["Mercury", "Venus", "Earth"],
    )

    df.plot.pie(subplots=True)

    plt.show()


plot()
