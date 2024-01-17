# Altair-Easeviz

***
This Python library is dedicated to providing resources for Vega-Altair, with the aim of enhancing the creation of
improved
and more accessible graphs. The development of this library involved a thorough exploration of both the Altair and
Vega-Lite APIs.

## Installation

***

The library and its dependencies can be easily installed, using:

```
pip install altair-easeviz
```

## Documentation

***
Documentation for this library can be found [here](https://miguelub.github.io/altair-easeviz/).

## Features

***

- Initial release of four accessible themes for Vega-Altair
- Generate description for charts added
- HTML with accessible functions added
- Models for creation and customization themes of vega-lite specification added

## Example

***
This next example shows how to enable one of our four themes.
More examples are available in our [documentation ](https://miguelub.github.io/altair-easeviz/p3-examples/).

![Bar Chart with accessible theme](docs/assets/basic_bar_chart_accessible.png)

```py
import altair as alt
import pandas as pd

# Enable Theme accessible_theme, dark_accessible_theme, filler_pattern_theme, print_theme
alt.themes.enable('accessible_theme')

# Define a Chart
source = pd.DataFrame({
    'a': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'],
    'b': [28, 55, 43, 91, 81, 53, 19, 87, 52]
})

alt.Chart(source).mark_bar().encode(
    x='a',
    y='b'
)
```
## Getting Help

***
For bugs and feature requests, please open a [Github Issue](https://github.com/MiguelUB/altair-easeviz/issues).
