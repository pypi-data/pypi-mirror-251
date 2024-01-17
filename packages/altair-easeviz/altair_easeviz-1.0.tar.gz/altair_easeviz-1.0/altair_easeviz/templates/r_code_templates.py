def r_code_bar_chart(x_axis, y_axis, chart_title, x_axis_title, y_axis_title):
    """
    This function will insert the data into a string that will be used in the R code

    :param x_axis: A List of either str, int or float
    :param y_axis: A list of numeric values int or float (preferably)
    :param chart_title: The title of the chart
    :param y_axis_title: Title of X axis
    :param x_axis_title: Title of Y axis
    :return: A string that describes the R code
    """
    x_axis = ', '.join(f'"{elemento}"' if isinstance(elemento, str) else str(elemento) for elemento in x_axis)
    y_axis = ', '.join(f'"{elemento}"' if isinstance(elemento, str) else str(elemento) for elemento in y_axis)
    return f"""
    library(ggplot2)
    library(BrailleR)
    

    # Data
    source <- data.frame(
      a = c({x_axis}),
      b = c({y_axis})
    )

    # Define chart
    acc_plot <- ggplot(source, aes(x = a, y = b)) +
    geom_bar(stat = "identity", fill = "blue", alpha = 0.7) +
    ggtitle("{chart_title}") +
    xlab("{x_axis_title}") +
    ylab("{y_axis_title}")

    # Capture description
    description <- capture.output(VI(acc_plot, Describe=TRUE))
    description
    """


def r_code_pie_chart(x_axis, y_axis, chart_title):
    """
    This function will insert the data into a string that will be used in the R code
    :param x_axis: A List of either str, int or float
    :param y_axis: A list of numeric values int or float (preferably)
    :param chart_title: The title of the chart
    :return: A string that describe the R code
    """
    x_axis = ', '.join(f'"{elemento}"' if isinstance(elemento, str) else str(elemento) for elemento in x_axis)
    y_axis = ', '.join(f'"{elemento}"' if isinstance(elemento, str) else str(elemento) for elemento in y_axis)
    print(x_axis, y_axis)
    return f"""
    library(ggplot2)
    library(BrailleR)

    # Data
    source <- data.frame(
      Categoria = c({x_axis}),
      Valor = c({y_axis})
    )

    # Define chart
    acc_plot <- ggplot(source, aes(x = "", y = Valor, fill = Categoria)) +
    geom_bar(width = 1, stat = "identity") +
    coord_polar("y") +
    ggtitle("{chart_title}") +
    theme_minimal()

    # Capture description
    description <- capture.output(VI(acc_plot, Describe=TRUE))
    description

    """


def r_code_scatter_plot(x_axis, y_axis, chart_title, x_axis_title, y_axis_title):
    """
    This function will insert the data into a string that will be used in the R code

    :param x_axis: A List of either str, int or float
    :param y_axis: A list of numeric values int or float (preferably)
    :param chart_title: The title of the chart
    :param x_axis_title: Title of X axis
    :param y_axis_title: Title of Y axis
    :return: A string that describes the R code
    """
    x_axis = ', '.join(f'"{elemento}"' if isinstance(elemento, str) else str(elemento) for elemento in x_axis)
    y_axis = ', '.join(f'"{elemento}"' if isinstance(elemento, str) else str(elemento) for elemento in y_axis)
    return f"""
    library(ggplot2)
    library(BrailleR)

    # Data
    source <- data.frame(
      x = c({x_axis}),
      y = c({y_axis})
    )

    

    # Define chart
    acc_plot <- invisible(ggplot(source, aes(x = x, y = y)) +
    geom_point(color = "blue", size = 3) +
    ggtitle("{chart_title}") +
    xlab("{x_axis_title}") +
    ylab("{y_axis_title}") +
    theme_minimal())
    

    # Capture description
    description <- capture.output(VI(acc_plot, Describe=TRUE))
    description

    """


def r_code_line_chart(x_axis, y_axis, chart_title, x_axis_title, y_axis_title):
    """
    This function will insert the data into a string that will be used in the R code

    :param x_axis: A List of either str, int or float
    :param y_axis: A list of numeric values int or float (preferably)
    :param chart_title: The title of the chart
    :param x_axis_title: Title of X axis
    :param y_axis_title: Title of Y axis
    :return: A string that describes the R code
    """
    x_axis = ', '.join(f'"{elemento}"' if isinstance(elemento, str) else str(elemento) for elemento in x_axis)
    y_axis = ', '.join(f'"{elemento}"' if isinstance(elemento, str) else str(elemento) for elemento in y_axis)
    return f"""
    library(ggplot2)
    library(BrailleR)

    # Data
    source <- data.frame(
      x = c({x_axis}),
      y = c({y_axis})
    )



    # Define chart
    acc_plot <- ggplot(source, aes(x = x, y = y)) +
    geom_line(color = "black", size = 2) +
    ggtitle("{chart_title}") +
    xlab("{x_axis_title}") +
    ylab("{y_axis_title}") 
    graphics.off()
    # Capture description
    description <- capture.output(VI(acc_plot, Describe=TRUE))
    description

    """
