from typing import List

import altair
import pyRserve
from altair import Chart

from altair_easeviz.templates import r_code_bar_chart, r_code_pie_chart, r_code_scatter_plot, \
    r_code_line_chart

def generate_description(chart: Chart, type_chart: str, axis_x: List, axis_y: List):
    """
        This function will generate a descripcion of a given chart and return a dict with all the parameters.
    It will return a dict with the error in case of fail

    :param axis_y:
    :param axis_x:
    :param chart: A Chart Altair object
    :param type_chart: "bar", "scatter", "line"
    :return: Dict with a description of the Chart
    """

    response = {"error": "The function did not work or even try to connect to R"}
    type_chart = type_chart.lower()
    chart_dict = chart.to_dict()
    chart_title = chart_dict['title'] if "title" in chart_dict else "Accesible Chart"
    x_axis_title = "X axis"
    y_axis_title = "Y axis"

    if 'x' in chart_dict['encoding']:
        x_axis_title = chart_dict['encoding']['field'] if "field" in chart_dict['encoding'] else x_axis_title
    if 'y' in chart_dict['encoding']:
        y_axis_title = chart_dict['encoding']['field'] if "field" in chart_dict['encoding'] else y_axis_title

    try:
        conn = pyRserve.connect()
    except Exception as e:
        response = {"error": e}
        print(f"Error executing R code: {e}")

    # Stablish connection with pyRserve
    try:

        # Execute chart in R
        if (type_chart == "barchart"):
            r_code = r_code_bar_chart(axis_x, axis_y, chart_title, x_axis_title, y_axis_title)
            response = {"res": conn.eval(r_code)}
        if (type_chart == "scatterplot"):
            r_code = r_code_scatter_plot(axis_x, axis_y, chart_title, x_axis_title, y_axis_title)
            response = {"res": conn.eval(r_code)}

        if (type_chart == "piechart"):
            r_code = r_code_pie_chart(axis_x, axis_y, chart_title)
            response = {"res": conn.eval(r_code)}

        if (type_chart == "linechart"):
            r_code = r_code_line_chart(axis_x, axis_y, chart_title, x_axis_title, y_axis_title)
            response = {"res": conn.eval(r_code)}

        # Reformat response
        if 'res' in response:
            response['res'] = '\n'.join(response['res'])
        # Close connection
        conn.close()
    # Return results
    except Exception as e:
        response = {"error": e.__str__()}
        print(f"Error executing R code: {e}")
    finally:
        # Cierra la conexión
        return response
