class DrawingType:
    # ----------------------
    # common types with data
    # ----------------------

    # Pandas all plots using single method
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.plot.html
    # https://pandas.pydata.org/docs/reference/api/pandas.Series.plot.html

    hist = "hist"
    # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.hist.html
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.hist.html
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.plot.hist.html
    # https://pandas.pydata.org/docs/reference/api/pandas.Series.hist.html
    # https://pandas.pydata.org/docs/reference/api/pandas.Series.plot.hist.html
    # https://seaborn.pydata.org/generated/seaborn.histplot.html

    line = "line"
    scatter = "scatter"
    pie = "pie"
    bar = "bar"

    # ---------------------------
    # common types (without data)
    # ---------------------------

    violin = "violin"
    heatmap = "heatmap"
    box = "box"
    dis = "dis"  # distribution plot (pandas' density and kde, seaborn' displot)

    # pandas only (without data)
    area = "area"
    hexbin = "hexbin"

    # seaborn only (without data)
    lm = "lm"
    cat = "cat"
