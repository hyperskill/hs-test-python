class DrawingType:
    # common types with data
    hist = "hist"
    line = "line"
    scatter = "scatter"
    pie = "pie"
    bar = "bar"

    # common types (without data)
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
