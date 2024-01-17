"""Here we define the type we will be using in each class, in order to create """

from typing import List

from typing_extensions import TypedDict


class Axis(TypedDict, total=False):
    """`axis`, `axisBand`, and `axisY` configurations."""

    domain: bool
    domainColor: str
    grid: bool
    gridCap: str
    gridColor: str
    gridDash: List[int]
    gridWidth: float
    labelColor: str
    labelFont: str
    labelFontSize: str
    labelPadding: int
    tickColor: str
    tickOpacity: float
    ticks: bool
    tickSize: int
    titleColor: str
    titleFont: str
    titleFontSize: int


class AxisBand(TypedDict):
    domain: bool
    labelPadding: int
    ticks: bool


class AxisY(TypedDict):
    domain: bool
    ticks: bool
    titleAlign: str
    titleAngle: int
    titleX: int
    titleY: int


class AxisX(TypedDict):
    domain: bool
    ticks: bool
    titleAlign: str
    titleAngle: int
    titleX: int
    titleY: int


class Legend(TypedDict):
    """`legend` configuration."""

    labelColor: str
    labelFont: str
    labelFontSize: int
    symbolSize: int
    titleColor: str
    titleFont: str
    titleFontSize: int
    titlePadding: int


class Mark(TypedDict, total=False):
    """`arc`, `bar`, `line`, `path`, `point`, `rect`, `rule`, `shape`, `text`, and `group` configurations."""

    color: str
    fill: str
    filled: bool
    font: str
    fontSize: int
    shape: str
    stroke: str
    strokeWidth: float


class ScaleRange(TypedDict, total=False):
    """Scale `range` configuration."""

    category: List[str]
    diverging: List[str]
    heatmap: List[str]
    ramp: List[str]


class Header(TypedDict):
    """`header` configuration."""

    labelColor: str
    labelFont: str
    labelFontSize: int
    titleColor: str
    titleFont: str
    titleFontSize: int


class Title(TypedDict):
    """`title` configuration."""

    anchor: str
    color: str
    font: str
    fontSize: int
    fontWeight: str
    offset: int
    subtitleColor: str
    subtitleFontSize: int


class View(TypedDict):
    """`view` configuration."""

    continuousHeight: int
    continuousWidth: int
    stroke: str


class Config(TypedDict, total=False):
    """Chart theme configuration."""

    axis: Axis
    axisBand: Axis
    axisY: Axis
    legend: Legend
    arc: Mark
    bar: Mark
    line: Mark
    path: Mark
    point: Mark
    rect: Mark
    rule: Mark
    shape: Mark
    text: Mark
    range: ScaleRange
    background: str
    group: Mark
    header: Header
    title: Title
    view: View


class Theme(TypedDict):
    """Wrapper for the chart theme configuration."""

    config: Config


class Categorical(TypedDict):
    """Categorical color scheme configurations."""

    paired: List[str]
    dark2: List[str]
    set2: List[str]
    ibm: List[str]
    wong: List[str]
    tol: List[str]
    set3: List[str]


class Diverging(TypedDict):
    """Diverging color scheme configurations."""

    bluered: List[str]
    orangepurple: List[str]
    pinkgreen: List[str]
    brownteal: List[str]


class Sequential(TypedDict):
    """Sequential color scheme configurations. For single and mult hue colors"""

    blues: List[str]
    greens: List[str]
    reds: List[str]
    oranges: List[str]
    purples: List[str]
    multihueblue: List[str]
    multihuered: List[str]
    multihuegreen: List[str]
    multihueorange: List[str]
    multihuepurple: List[str]
    grays: List[str]


class ColorScheme(TypedDict):
    """Color scheme configuration."""

    categorical: Categorical
    diverging: Diverging
    sequential: Sequential


class Colors(TypedDict):
    """Colors token."""

    arc: str
    axis: str
    background: str
    mark: str
    text: str
    schemes: ColorScheme


"""
Color token

Colors should be ordered from lightest to darkest, where '00' is the lightest color and
'60' is  the darkest color.
"""
Color = TypedDict(
    "Color",
    {"00": str, "10": str, "20": str, "30": str, "40": str, "50": str, "60": str},
)
