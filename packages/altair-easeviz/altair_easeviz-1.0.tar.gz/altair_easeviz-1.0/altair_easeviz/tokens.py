"""Design tokens for the theme and standalone use.
"""

from typing import Dict

from altair_easeviz.types_theme import Color, Colors

FONT: str = "Roboto, Arial, sans-serif"

FONT_SIZES: Dict[str, int] = {"xsm": 10, "sm": 14, "md": 18, "lg": 22}

OPACITIES: Dict[str, float] = {"md": 0.5}

SYMBOL_SIZE: int = 40

STROKE_WIDTHS: Dict[str, float] = {"sm": 0.5, "md": 1, "lg": 2}

SPACING: Dict[str, int] = {"xs": 1, "sm": 2, "md": 4, "lg": 8, "xl": 20}

COLOR_PRIMITIVES: Dict[str, Color] = {
    "black": "#232323",
    "white": "#FFFFFF",
    "blue": {
        "00": "#a3d1ef",
        "10": "#6db5e6",
        "20": "#369adc",
        "30": "#1f78b4",
        "40": "#16547e",
        "50": "#0c2f47",
    },
    "red": {
        "00": "#FBEAEA",
        "10": "#FBEAEA",
        "20": "#E58686",
        "30": "#FBEAEA",
        "40": "#D32F2F",
        "50": "#942121",
        "60": "#811D1D",
    },
    "green": {
        "00": "#AEDF8B",
        "10": "#79d973",
        "20": "#49cb41",
        "30": "#33A02C",
        "40": "#236e1e",
        "50": "#133c11",
    },
    "yellow": {
        "00": "#FFF9E6",
        "10": "#FFE796",
        "20": "#FFDD6B",
        "30": "#FFCE2B",
        "40": "#FFC400",
        "50": "#B38900",
        "60": "#7F6202",
    },
    "lavender": {
        "00": "#F5EFFD",
        "10": "#D4BDF5",
        "20": "#C2A2F1",
        "30": "#A87AEA",
        "40": "#965FE6",
        "50": "#6943A1",
        "60": "#5C3A8C",
    },
    "teal": {
        "00": "#E6F6F5",
        "10": "#96D9D7",
        "20": "#6BCAC7",
        "30": "#2BB3AE",
        "40": "#00A39E",
        "50": "#00726F",
        "60": "#006360",
    },
    "pink": {
        "00": "#fdd7d6",
        "10": "#FB9A99",
        "20": "#f95d5c",
    },
    "orange": {
        "00": "#ffd7be",
        "10": "#ffb07f",
        "20": "#ff883f",
        "30": "#fe6100",
        "40": "#be4900",
        "50": "#7f3000",
        "60": "#3f1800",
    },
    "neutral": {
        "00": "#F0F1F6",
        "10": "#E1E2E7",
        "20": "#B3B7C4",
        "30": "#666F89",
        "40": "#4D5776",
        "50": "#19274E",
        "60": "#000F3A",
    },
}

COLORS: Colors = {
    "arc": "#FFFFFF",
    "axis": COLOR_PRIMITIVES["neutral"]["60"],
    "background": "#E9E8E8",
    "mark": COLOR_PRIMITIVES["blue"]["40"],
    "text": COLOR_PRIMITIVES["neutral"]["50"],
    "schemes": {
        "categorical": {
            "paired": ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c'],
            # Suitable for a dark background
            "dark2": ['#1b9e77', '#d95f02', '#7570b3', '#e7298a', "#609B1C"],  # Suitable for a white and dark background
            "set2": ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854'],  # Suitable for a dark background
            'wong': ['#E69F00', '#56B4E9', '#009E73', '#F0E442', '#0072B2', '#D55E00', "#CC79A7"],
            # Suitable for a dark background
            'tol': ['#332288', '#117733', '#44AA99', '#88CCEE', '#DDCC77', '#CC6677', "#AF469D", "#882255"],
            # Not suitable for white or dark background acording to 3:1 ratio of WCGA still is usefull for color blind people
            "ibm": ['#648FFF', '#FFB000', '#785EF0', '#FE6100', '#DC267F'],
            # Suitable for dark backgrounds and maybe white if the yellow is not prominent
            'set3': ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072']  # Suitable for dark backgrounds
        },
        "diverging": {
            "bluered": ['#a50026', '#d73027', '#f46d43', '#fdae61', '#fee090', '#ffffbf', '#e0f3f8', '#abd9e9',
                        '#74add1', '#4575b4', '#313695'],
            "orangepurple": ['#7f3b08', '#b35806', '#e08214', '#fdb863', '#fee0b6', '#f7f7f7', '#d8daeb', '#b2abd2',
                             '#8073ac', '#542788', '#2d004b'],
            "pinkgreen": ['#8e0152', '#c51b7d', '#de77ae', '#f1b6da', '#fde0ef', '#f7f7f7', '#e6f5d0', '#b8e186',
                          '#7fbc41', '#4d9221', '#276419'],
            "brownteal": ['#543005', '#8c510a', '#bf812d', '#dfc27d', '#f6e8c3', '#f5f5f5', '#c7eae5', '#80cdc1',
                          '#35978f', '#01665e', '#003c30']
        },

        "sequential": {
            "blues": ['#08306b', '#08519c', '#2171b5', '#4292c6', '#6baed6', '#9ecae1', '#c6dbef', '#deebf7',
                      '#f7fbff'],
            "greens": ['#00441b', '#006d2c', '#238b45', '#41ab5d', '#74c476', '#a1d99b', '#c7e9c0', '#e5f5e0',
                       '#f7fcf5']
            ,
            "reds": ['#67000d', '#a50f15', '#cb181d', '#ef3b2c', '#fb6a4a', '#fc9272', '#fcbba1', '#fee0d2', '#fff5f0'],

            "purples": ['#fcfbfd', '#efedf5', '#dadaeb', '#bcbddc', '#9e9ac8', '#807dba', '#6a51a3', '#54278f',
                        '#3f007d'],
            "oranges": ['#7f2704', '#a63603', '#d94801', '#f16913', '#fd8d3c', '#fdae6b', '#fdd0a2', '#fee6ce',
                        '#fff5eb'],
            "multihueblue": ['#ffffd9', '#edf8b1', '#c7e9b4', '#7fcdbb', '#41b6c4', '#1d91c0', '#225ea8', '#253494',
                             '#081d58'],
            "multihuegreen": ['#ffffe5', '#f7fcb9', '#d9f0a3', '#addd8e', '#78c679', '#41ab5d', '#238443', '#006837',
                              '#004529'],
            "multihuered": ['#ffffcc', '#ffeda0', '#fed976', '#feb24c', '#fd8d3c', '#fc4e2a', '#e31a1c', '#bd0026',
                            '#800026'],
            "multihuepurple": ['#fff7f3', '#fde0dd', '#fcc5c0', '#fa9fb5', '#f768a1', '#dd3497', '#ae017e', '#7a0177',
                               '#49006a'],
            "multihueorange": ['#ffffe5', '#fff7bc', '#fee391', '#fec44f', '#fe9929', '#ec7014', '#cc4c02', '#993404',
                               '#662506'],
            "grays": [
                COLOR_PRIMITIVES["neutral"]["60"],
                COLOR_PRIMITIVES["neutral"]["50"],
                COLOR_PRIMITIVES["neutral"]["40"],
                COLOR_PRIMITIVES["neutral"]["30"],
                COLOR_PRIMITIVES["neutral"]["20"],
                COLOR_PRIMITIVES["neutral"]["10"],
                COLOR_PRIMITIVES["neutral"]["00"],
            ],
        },
    },
}
