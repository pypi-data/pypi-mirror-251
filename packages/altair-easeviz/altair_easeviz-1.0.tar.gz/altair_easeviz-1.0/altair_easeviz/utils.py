import json

from altair import Chart, LayerChart, HConcatChart, VConcatChart, FacetChart, RepeatChart
from jinja2 import Template

from altair_easeviz.templates import accesible_template


def create_accessible_scheme(chart: Chart, filename: str = 'test', description: str = None):
    """
    This function will create an HTML file in the root of the project, this HTML file will contain the vega lite style
    graphic using the information from the vega-altair Chart passed.
    The new HTML file contains some option for the user to change the color scheme in order to be more accessible

    :param chart:Chart This is a vega-altair Chart object
    :param filename:str Name of the new HTML file
    :param description:str A description to instep in the attribute aria-label for the screen readers
    """
    chart_json = json.loads(chart.to_json())
    html_path = filename + ".html"
    template = Template(accesible_template)
    description_chart = description
    chart_title = "Accessible  Graph"
    description_given = False
    multi_chart = False
    if description_chart is not None:
        description_given = True
        description_html = description_chart.replace("\n", "<br>")
    else:
        description_chart = "This is a graph made with vega-altair and altair-easeviz"
        description_html = None

    if isinstance(chart, VConcatChart) or isinstance(chart, HConcatChart) or \
            isinstance(chart, LayerChart) or isinstance(chart, FacetChart) or isinstance(chart, RepeatChart):
        multi_chart = True

    template_html = template.render(chart=chart_json, description=description_chart, description_html=description_html,
                                    title=chart_title,
                                    multi_chart=multi_chart, description_given=description_given)
    with open(html_path, "w") as file:
        file.write(template_html)
    print("The HTML file has been created in", html_path)
