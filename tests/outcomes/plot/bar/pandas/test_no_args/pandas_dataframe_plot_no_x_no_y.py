def plot():
    try:
        import matplotlib.pyplot as plt
        import pandas as pd
    except ModuleNotFoundError:
        return

    df = pd.DataFrame({"lab": [2, 3, 4, 5, 6], "val": [3, 4, 5, 6, 7]})

    df.plot.bar()

    plt.show()


plot()
