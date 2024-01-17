from altair_easeviz.tokens import COLORS, STROKE_WIDTHS, FONT, FONT_SIZES
from altair_easeviz.types_theme import Mark


# https://github.com/altair-viz/altair/tree/e1bb266f91bd743c815fce9908d03d3bb1ad13fc/doc/user_guide/marks
class MarkArkModel():

    def __init__(self, **kwargs):
        self._required_params = {
            'stroke': str, 'strokeWidth': float
        }

        # Establecer valores predeterminados

        self.stroke = kwargs.get('stroke', COLORS['arc'])
        self.strokeWidth = kwargs.get('strokeWidth', STROKE_WIDTHS['md'])

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

    def create_mark_ark(self):
        new_mark = Mark(
            stroke=self.stroke,
            strokeWidth=self.strokeWidth
        )
        return new_mark


class MarkBarModel():

    def __init__(self, **kwargs):
        self._required_params = {
            'fill': str, 'stroke': str
        }

        # Establecer valores predeterminados

        self.fill = kwargs.get('fill', COLORS['mark'])
        self.stroke = kwargs.get('stroke', None)

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

    def create_mark_bar(self):
        new_mark = Mark(
            fill=self.fill,
            stroke=self.stroke
        )
        return new_mark


class MarkLineModel():

    def __init__(self, **kwargs):
        self._required_params = {
            'stroke': str, 'strokeWidth': float
        }

        # Establecer valores predeterminados
        self.stroke = kwargs.get('stroke', COLORS['mark'])
        self.strokeWidth = kwargs.get('strokeWidth', STROKE_WIDTHS['lg'])

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

    def create_mark_line(self):
        new_mark = Mark(
            stroke=self.stroke,
            strokeWidth=self.strokeWidth
        )
        return new_mark


class MarkPathModel():

    def __init__(self, **kwargs):
        self._required_params = {
            'stroke': str, 'strokeWidth': float
        }

        # Establecer valores predeterminados
        self.stroke = kwargs.get('stroke', COLORS['mark'])
        self.strokeWidth = kwargs.get('strokeWidth', STROKE_WIDTHS['sm'])

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

    def create_mark_path(self):
        new_mark = Mark(
            stroke=self.stroke,
            strokeWidth=self.strokeWidth
        )
        return new_mark


class MarkPointModel():

    def __init__(self, **kwargs):
        self._required_params = {
            'fill': str, 'filled': bool, 'shape': str,
        }

        # Establecer valores predeterminados
        self.fill = kwargs.get('fill', COLORS['mark'])
        self.filled = kwargs.get('filled', True)
        self.shape = kwargs.get('shape', 'circle')  # circle square cross diamond triangle-up triangle-right

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

    def create_mark_point(self):
        new_mark = Mark(
            fill=self.fill,
            filled=self.filled,
            shape=self.shape,
        )
        return new_mark


class MarkRectModel():

    def __init__(self, **kwargs):
        self._required_params = {
            'fill': str
        }

        # Establecer valores predeterminados
        self.fill = kwargs.get('fill', COLORS['mark'])

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

    def create_mark_rect(self):
        new_mark = Mark(
            fill=self.fill,
        )
        return new_mark


class MarkRuleModel():

    def __init__(self, **kwargs):
        self._required_params = {
            'stroke': str,
        }

        # Establecer valores predeterminados
        self.stroke = kwargs.get('shape', COLORS["axis"])

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

    def create_mark_rule(self):
        new_mark = Mark(
            stroke=self.stroke,
        )
        return new_mark


class MarkShapeModel():

    def __init__(self, **kwargs):
        self._required_params = {
            'stroke': str,
        }

        # Establecer valores predeterminados
        self.stroke = kwargs.get('stroke', COLORS["mark"])

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

    def create_mark_shape(self):
        new_mark = Mark(
            stroke=self.stroke,
        )
        return new_mark


class MarkTextModel():

    def __init__(self, **kwargs):
        self._required_params = {
            'color': str, 'font': str, 'fontSize': int
        }

        # Establecer valores predeterminados
        self.color = kwargs.get('color', COLORS["text"])
        self.font = kwargs.get('font', FONT)
        self.fontSize = kwargs.get('fontSize', FONT_SIZES["sm"])

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

    def create_mark_text(self):
        new_mark = Mark(
            color=self.color,
            font=self.font,
            fontSize=self.fontSize,

        )
        return new_mark
