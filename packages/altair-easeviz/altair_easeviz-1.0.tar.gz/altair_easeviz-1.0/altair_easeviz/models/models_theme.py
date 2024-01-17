from typing import List

from altair_easeviz.models.models_axis import AxisModel
from altair_easeviz.models.models_config import ConfigModel
from altair_easeviz.models.models_header import HeaderModel
from altair_easeviz.models.models_legend import LegendModel
from altair_easeviz.models.models_mark import *
from altair_easeviz.models.models_range import RangeModel
from altair_easeviz.models.models_title import TitleModel
from altair_easeviz.models.models_view import ViewModel
from altair_easeviz.tokens import COLORS, FONT, FONT_SIZES, OPACITIES, SPACING, \
    COLOR_PRIMITIVES
from altair_easeviz.types_theme import Colors
import altair as alt


class ModelTheme:

    def __init__(self, name_theme: str, text_color: str, axis_color: str, mark_color: str,
                 background_color: str, grid: bool):
        self.colors: Colors = {'arc': '#FFFFFF', 'axis': COLORS['axis'], 'background': COLORS['background'],
                               'text': COLORS['text'],
                               'mark': COLOR_PRIMITIVES["lavender"]["40"],
                               "schemes": {
                                   "categorical": COLORS['schemes']['categorical']['dark2'],
                                   "diverging": COLORS['schemes']['diverging']['bluered'],
                                   "sequential": COLORS['schemes']['sequential']['blues']}}
        self.font_size: FONT_SIZES = {'xsm': FONT_SIZES['xsm'], 'sm': FONT_SIZES['sm'], 'md': FONT_SIZES['md'],
                                      'lg': FONT_SIZES['lg']}
        self.spacing: SPACING = {'sm': SPACING['sm'], 'md': SPACING['md'], 'xl': SPACING['xl']}
        self.name_theme = name_theme
        self.colors['background'] = background_color
        self.colors['text'] = text_color
        self.colors['axis'] = axis_color
        self.colors['mark'] = mark_color
        self.grid = grid

        self.axis_config = AxisModel(gridColor=self.colors['axis'], labelColor=self.colors['text'],
                                     labelFontSize=self.font_size['xsm'], tickOpacity=1.0,
                                     gridOpacity=0.3, grid=self.grid,
                                     domainColor=self.colors['text'],
                                     tickSize=self.spacing['md'],
                                     tickColor=self.colors['axis'],
                                     titleColor=self.colors['text'],
                                     titleFontSize=self.font_size['sm']).create_axis()

        self.header_config = HeaderModel(labelColor=self.colors['text'], labelFontSize=self.font_size['sm'],
                                         titleColor=self.colors['text'],
                                         titleFontSize=self.font_size['md']).create_header()

        self.legend_config = LegendModel(labelColor=self.colors['text'], labelFontSize=self.font_size['sm'],
                                         titleColor=self.colors['text'],
                                         titleFontSize=self.font_size['sm'],
                                         titlePadding=self.spacing['md']).create_legend()

        self.title_config = TitleModel(color=self.colors["text"], fontSize=self.font_size["lg"],
                                       subtitleColor=self.colors['text'],
                                       subtitleFontSize=self.font_size['md']).create_title()
        self.view_config = ViewModel(stroke='tan').create_view()

        # Color Schemes config
        self.range_config = RangeModel(category=self.colors['schemes']["categorical"],
                                       diverging=self.colors['schemes']["diverging"],
                                       heatmap=self.colors['schemes']["sequential"],
                                       ramp=self.colors['schemes']["sequential"]).create_range()

        # Marks config
        self.arc_config = MarkArkModel(stroke=self.colors['arc']).create_mark_ark()
        self.bar_config = MarkBarModel(fill=self.colors['mark'], stroke=self.colors['arc']).create_mark_bar()
        self.line_config = MarkLineModel(stroke=self.colors['mark']).create_mark_line()
        self.path_config = MarkPathModel(stroke=self.colors['mark']).create_mark_path()
        self.point_config = MarkPointModel(fill=self.colors["mark"], filled=True).create_mark_point()
        self.rect_config = MarkRectModel(fill=self.colors["mark"]).create_mark_rect()
        self.rule_config = MarkRuleModel(stroke=self.colors['mark']).create_mark_rule()
        self.shape_config = MarkShapeModel(stroke=self.colors['mark']).create_mark_shape()
        self.text_config = MarkTextModel(color=self.colors["text"], fontSize=self.font_size['sm']).create_mark_text()

        self.config = ConfigModel(background=self.colors['background'],
                                  axis=self.axis_config, header=self.header_config,
                                  legend=self.legend_config, range=self.range_config,
                                  title=self.title_config, view=self.view_config,
                                  arc=self.arc_config, bar=self.bar_config,
                                  line=self.line_config, path=self.path_config,
                                  point=self.point_config, rect=self.rect_config,
                                  rule=self.rule_config, shape=self.shape_config,
                                  text=self.text_config)

    def get_theme(self):
        self.axis_config = AxisModel(gridColor=self.colors['axis'], labelColor=self.colors['text'],
                                     labelFontSize=self.font_size['xsm'],
                                     tickOpacity=1.0,
                                     gridOpacity=0.3, grid=self.grid,
                                     domainColor=self.colors['text'],
                                     tickSize=self.spacing['md'],
                                     tickColor=self.colors['axis'],
                                     titleColor=self.colors['text'],
                                     titleFontSize=self.font_size['sm']).create_axis()

        self.header_config = HeaderModel(labelColor=self.colors['text'], labelFontSize=self.font_size['sm'],
                                         titleColor=self.colors['text'],
                                         titleFontSize=self.font_size['md']).create_header()

        self.legend_config = LegendModel(labelColor=self.colors['text'], labelFontSize=self.font_size['sm'],
                                         titleColor=self.colors['text'],
                                         titleFontSize=self.font_size['sm'],
                                         titlePadding=self.spacing['md']).create_legend()

        self.title_config = TitleModel(color=self.colors["text"], fontSize=self.font_size["lg"],
                                       subtitleColor=self.colors['text'],
                                       subtitleFontSize=self.font_size['md']).create_title()
        self.view_config = ViewModel(stroke='tan').create_view()

        # Color Schemes config
        self.range_config = RangeModel(category=self.colors['schemes']["categorical"],
                                       diverging=self.colors['schemes']["diverging"],
                                       heatmap=self.colors['schemes']["sequential"],
                                       ramp=self.colors['schemes']["sequential"]).create_range()

        # Marks config
        self.arc_config = MarkArkModel(stroke=self.colors['arc']).create_mark_ark()
        self.bar_config = MarkBarModel(fill=self.colors['mark'], stroke=self.colors['arc']).create_mark_bar()
        self.line_config = MarkLineModel(stroke=self.colors['mark']).create_mark_line()
        self.path_config = MarkPathModel(stroke=self.colors['mark']).create_mark_path()
        self.point_config = MarkPointModel(fill=self.colors["mark"], filled=True).create_mark_point()
        self.rect_config = MarkRectModel(fill=self.colors["mark"]).create_mark_rect()
        self.rule_config = MarkRuleModel(stroke=self.colors['mark']).create_mark_rule()
        self.shape_config = MarkShapeModel(stroke=self.colors['mark']).create_mark_shape()
        self.text_config = MarkTextModel(color=self.colors["text"], fontSize=self.font_size['sm']).create_mark_text()
        self.config = ConfigModel(background=self.colors['background'],
                                  axis=self.axis_config, header=self.header_config,
                                  legend=self.legend_config, range=self.range_config,
                                  title=self.title_config, view=self.view_config,
                                  arc=self.arc_config, bar=self.bar_config,
                                  line=self.line_config, path=self.path_config,
                                  point=self.point_config, rect=self.rect_config,
                                  rule=self.rule_config, shape=self.shape_config,
                                  text=self.text_config)

        return self.config.create_full_config()

    def getName(self):
        return self.name_theme

    def change_background_color(self, new_color):
        """
        Change the background of the graphic with a color, then re register the theme in altair.themes
        :param new_color: A color given in Hexadecimal ex. #FFFFFF
        """
        self.colors['background'] = new_color
        alt.themes.register(self.name_theme, self.get_theme)

    def change_mark_color(self, new_color):
        """
        Change de color of the marks like bars,lines, points, etc. when no z axis is given, then reregister the theme
        in altair.themes
        :param new_color: A color given in Hexadecimal ex. #185ABD
        """
        self.colors['mark'] = new_color
        alt.themes.register(self.name_theme, self.get_theme)

    def change_text_color(self, new_color):
        """
        Change the color of all text in the graph, then re register the theme in altair.themes
        :param new_color: A color given in Hexadecimal ex. #000000
        """
        self.colors['text'] = new_color
        alt.themes.register(self.name_theme, self.get_theme)

    def increase_font_size(self, number: int):
        """
        Increase the size of the font by a given number, since all text most by hierarchical the ratio is kept and all
        fonts increase sizes, then re register the theme in altair.themes
        :param number: A int value greater than 0
        """
        if number >= 0:
            self.font_size["xsm"] += number
            self.font_size["sm"] += number
            self.font_size["md"] += number
            self.font_size["lg"] += number
            alt.themes.register(self.name_theme, self.get_theme)

    def decrease_font_size(self, number: int):
        """
        Decrease the size of the font by a given number, since all text most by hierarchical the ratio is kept and all
        fonts decrease sizes, then re register the theme in altair.themes
        :param number: A int value greater than 0
        """
        if number >= 0:
            self.font_size["xsm"] -= number
            self.font_size["sm"] -= number
            self.font_size["md"] -= number
            self.font_size["lg"] -= number

            if self.font_size['xsm'] < 0:
                self.font_size["xsm"] = 0

            if self.font_size['sm'] < 0:
                self.font_size["sm"] = 0
            if self.font_size['md'] < 0:
                self.font_size["md"] = 0
            if self.font_size['lg'] < 0:
                self.font_size["lg"] = 0
            alt.themes.register(self.name_theme, self.get_theme)

    def change_categorical_scheme(self, scheme: List[str]):
        """
        Change the categorical color scheme, then re register the theme in altair.themes
        :param scheme: A list of color in Hexadecimal like ['#123abd', '#ECB178']
        """
        self.colors['schemes']['categorical'] = scheme
        alt.themes.register(self.name_theme, self.get_theme)

    def change_sequential_scheme(self, scheme: List[str]):
        """
        Change the sequential color scheme, then re register the theme in altair.themes
        :param scheme: A list of color in Hexadecimal like ['#123abd', '#ECB178']
        """
        self.colors['schemes']['sequential'] = scheme
        alt.themes.register(self.name_theme, self.get_theme)

    def change_color_line(self, color_line):
        """
        Change the color of all lines in the graph like the grid, ticks, and domain, this no include the mark line
        :param color_line: A color in hexadecimal ex. #000000
        """
        self.colors['axis'] = color_line
        alt.themes.register(self.name_theme, self.get_theme)

    def change_grid_show(self):
        """
        Change if the grid is shown or not
        """
        self.grid = not self.grid
        alt.themes.register(self.name_theme, self.get_theme)


class AccessibleTheme(ModelTheme):
    def __init__(self):
        super().__init__('accessible_theme', COLOR_PRIMITIVES["black"], COLOR_PRIMITIVES["black"],
                         COLOR_PRIMITIVES["blue"]['30'], COLOR_PRIMITIVES["white"], False)


class DarkAccessibleTheme(ModelTheme):
    def __init__(self):
        super().__init__('dark_accessible_theme', COLOR_PRIMITIVES["white"], COLOR_PRIMITIVES["white"],
                         COLOR_PRIMITIVES["blue"]['30'], COLOR_PRIMITIVES["black"], False)
        self.change_categorical_scheme(COLORS["schemes"]['categorical']['paired'])

    def change_categorical_scheme(self, scheme: List[str]):
        super().change_categorical_scheme(scheme)


class FillerPatternTheme(ModelTheme):
    def __init__(self):
        super().__init__('filler_pattern_theme', COLOR_PRIMITIVES["black"], COLOR_PRIMITIVES["black"],
                         COLOR_PRIMITIVES["blue"]['30'], COLOR_PRIMITIVES["white"], False)
        self.change_categorical_scheme(
            ["url(#red-heart)", "url(#blue-rain)", "url(#green-leaf)", "url(#purple-grapes)", "url(#orange-orange)",
             "url(#yellow-star)", "url(#brown-chocolate)", "url(#pink-donut)", "url(#grey-wrench)", ])

    def change_categorical_scheme(self, scheme: List[str]):
        super().change_categorical_scheme(scheme)


class PrintFriendlyTheme(ModelTheme):
    def __init__(self):
        super().__init__('print_theme', COLOR_PRIMITIVES["black"], COLOR_PRIMITIVES["black"],
                         COLOR_PRIMITIVES["blue"]['30'], COLOR_PRIMITIVES["white"], False)
        self.change_categorical_scheme(COLORS["schemes"]['categorical']['set3'])

    def change_categorical_scheme(self, scheme: List[str]):
        super().change_categorical_scheme(scheme)
