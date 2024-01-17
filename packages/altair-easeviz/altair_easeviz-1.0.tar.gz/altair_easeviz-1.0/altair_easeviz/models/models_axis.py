from altair_easeviz.tokens import COLORS, STROKE_WIDTHS, FONT, SPACING, OPACITIES, FONT_SIZES
from altair_easeviz.types_theme import Axis, AxisBand, AxisY, AxisX


class AxisModel():

    def __init__(self, **kwargs):

        self._required_params = {
            'domain': bool, 'domainColor': str, 'grid': bool, 'gridCap': str, 'gridColor': str,
            'gridDash': list, 'gridWidth': float, 'labelColor': str, 'labelFont': str,
            'labelFontSize': int,
            'labelPadding': int, 'tickColor': str, 'tickOpacity': float, 'ticks': bool,
            'tickSize': int, 'titleColor': str, 'titleFont': str, 'titleFontSize': int
        }

        # Establecer valores predeterminados
        self.domain = kwargs.get('domain', True)
        self.domainColor = kwargs.get('domainColor', COLORS["axis"])
        self.grid = kwargs.get('grid', True)
        self.gridCap = kwargs.get('gridCap', 'round')  # round, butt, square,
        self.gridColor = kwargs.get('gridColor', COLORS["axis"])
        self.gridDash = kwargs.get('gridDash', [1, 1])
        self.gridWidth = kwargs.get('gridWidth', STROKE_WIDTHS["sm"])
        self.labelColor = kwargs.get('labelColor', COLORS["axis"])
        self.labelFont = kwargs.get('labelFont', FONT)
        self.labelFontSize = kwargs.get('labelFontSize', FONT_SIZES["xsm"])
        self.labelPadding = kwargs.get('labelPadding', SPACING["sm"])
        self.tickColor = kwargs.get('tickColor', COLORS["axis"])
        self.tickOpacity = kwargs.get('tickOpacity', OPACITIES["md"])
        self.ticks = kwargs.get('ticks', True)
        self.tickSize = kwargs.get('tickSize', SPACING["md"])
        self.titleColor = kwargs.get('titleColor', COLORS['text'])
        self.titleFont = kwargs.get('titleFont', FONT)
        self.titleFontSize = kwargs.get('titleFontSize', FONT_SIZES["sm"])

        # Actualizar atributos con kwargs
        self.__dict__.update(kwargs)

        # Verificar tipos de datos para los parámetros obligatorios
        for param, expected_type in self._required_params.items():
            if param in kwargs and not isinstance(getattr(self, param), expected_type):
                raise TypeError(f"Se esperaba '{param}' como tipo {expected_type}.")

        # Verificar que los parámetros obligatorios tengan valores
        missing_params = [param for param, expected_type in self._required_params.items() if
                          getattr(self, param, None) is None]
        if missing_params:
            raise ValueError(
                f"Los siguientes parámetros son obligatorios y no fueron proporcionados: {missing_params}")

    def create_axis(self):
        new_axis = Axis(
            domain=self.domain,
            domainColor=self.domainColor,
            grid=self.grid,
            gridCap=self.gridCap,
            gridColor=self.gridColor,
            gridDash=self.gridDash,
            gridWidth=self.gridWidth,
            labelColor=self.labelColor,
            labelFont=self.labelFont,
            labelFontSize=self.labelFontSize,
            labelPadding=self.labelPadding,
            tickColor=self.tickColor,
            tickOpacity=self.tickOpacity,
            ticks=self.ticks,
            tickSize=self.tickSize,
            titleColor=self.titleColor,
            titleFont=self.titleFont,
            titleFontSize=self.titleFontSize
        )
        return new_axis


class AxisBandModel():

    def __init__(self, **kwargs):

        self._required_params = {
            'domain': bool, 'labelPadding': int, 'ticks': bool
        }
        # Establecer valores predeterminados
        self.domain = kwargs.get('domain', True)
        self.labelPadding = kwargs.get('labelPadding', SPACING["sm"])
        self.ticks = kwargs.get('ticks', False)

        # Actualizar atributos con kwargs
        self.__dict__.update(kwargs)

        # Verificar tipos de datos para los parámetros obligatorios
        for param, expected_type in self._required_params.items():
            if param in kwargs and not isinstance(getattr(self, param), expected_type):
                raise TypeError(f"Se esperaba '{param}' como tipo {expected_type}.")

        # Verificar que los parámetros obligatorios tengan valores
        missing_params = [param for param, expected_type in self._required_params.items() if
                          getattr(self, param, None) is None]
        if missing_params:
            raise ValueError(
                f"Los siguientes parámetros son obligatorios y no fueron proporcionados: {missing_params}")

    def create_axis_band(self):
        new_axis_band = AxisBand(
            domain=self.domain,
            labelPadding=self.labelPadding,
            ticks=self.ticks,
        )
        return new_axis_band


class AxisYModel():

    def __init__(self, **kwargs):
        self._required_params = {
            'domain': bool, 'ticks': bool, 'titleAlign': str,
            'titleAngle': int, 'titleX': int, 'titleY': int
        }

        # Establecer valores predeterminados
        self.domain = kwargs.get('domain', False)
        self.ticks = kwargs.get('ticks', True)
        self.titleAlign = kwargs.get('titleAlign', 'left')
        self.titleAngle = kwargs.get('titleAngle', 0)
        self.titleX = kwargs.get('titleX', -20)
        self.titleY = kwargs.get('titleY', -10)

        # Actualizar atributos con kwargs
        self.__dict__.update(kwargs)

        # Verificar tipos de datos para los parámetros obligatorios
        for param, expected_type in self._required_params.items():
            if param in kwargs and not isinstance(getattr(self, param), expected_type):
                raise TypeError(f"Se esperaba '{param}' como tipo {expected_type}.")

        # Verificar que los parámetros obligatorios tengan valores
        missing_params = [param for param, expected_type in self._required_params.items() if
                          getattr(self, param, None) is None]
        if missing_params:
            raise ValueError(
                f"Los siguientes parámetros son obligatorios y no fueron proporcionados: {missing_params}")

    def create_axis_y(self):
        new_axis_y = AxisY(
            domain=self.domain,
            ticks=self.ticks,
            titleAlign=self.titleAlign,
            titleAngle=self.titleAngle,
            titleX=self.titleX,
            titleY=self.titleY
        )
        return new_axis_y


class AxisXModel():

    def __init__(self, **kwargs):
        self._required_params = {
            'domain': bool, 'ticks': bool, 'titleAlign': str,
            'titleAngle': int, 'titleX': int, 'titleY': int
        }

        # Establecer valores predeterminados
        self.domain = kwargs.get('domain', False)
        self.ticks = kwargs.get('ticks', True)
        self.titleAlign = kwargs.get('titleAlign', 'left')
        self.titleAngle = kwargs.get('titleAngle', 0)
        self.titleX = kwargs.get('titleX', -20)
        self.titleY = kwargs.get('titleY', -10)

        # Actualizar atributos con kwargs
        self.__dict__.update(kwargs)

        # Verificar tipos de datos para los parámetros obligatorios
        for param, expected_type in self._required_params.items():
            if param in kwargs and not isinstance(getattr(self, param), expected_type):
                raise TypeError(f"Se esperaba '{param}' como tipo {expected_type}.")

        # Verificar que los parámetros obligatorios tengan valores
        missing_params = [param for param, expected_type in self._required_params.items() if
                          getattr(self, param, None) is None]
        if missing_params:
            raise ValueError(
                f"Los siguientes parámetros son obligatorios y no fueron proporcionados: {missing_params}")

    def create_axis_x(self):
        new_axis_x = AxisX(
            domain=self.domain,
            ticks=self.ticks,
            titleAlign=self.titleAlign,
            titleAngle=self.titleAngle,
            titleX=self.titleX,
            titleY=self.titleY
        )
        return new_axis_x
