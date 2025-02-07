def plot():
    try:
        import matplotlib.pyplot as plt
        import pandas as pd

    except ModuleNotFoundError:
        return

    df = pd.DataFrame([[1, 2], [2, 6]], columns=["length", "width"])
    df.plot.scatter(x="length", y="width", c="DarkBlue")

    df.plot(kind="scatter", x="length", y="width", c="DarkBlue")

    plt.show()


plot()
