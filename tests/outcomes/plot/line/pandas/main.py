def plot():
    try:
        import matplotlib.pyplot as plt
        import pandas as pd
    except ModuleNotFoundError:
        return

    s = pd.Series([1, 3, 2])
    s.plot.line()
    s.plot(kind="line")

    df = pd.DataFrame({"a": [1, 3, 2], "b": [1, 3, 2]}, index=[2, 4, 6])
    df.plot.line()

    plt.show()


plot()
