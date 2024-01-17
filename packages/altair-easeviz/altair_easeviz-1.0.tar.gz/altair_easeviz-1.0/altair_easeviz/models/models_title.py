from altair_easeviz.tokens import COLORS, FONT, FONT_SIZES, SPACING
from altair_easeviz.types_theme import Title


class TitleModel():

    def __init__(self, **kwargs):
        self._required_params = {
            'anchor': str,
            'color': str,
            'font': str,
            'fontSize': int,
            'fontWeight': str,
            'offset': int,
            'subtitleColor': str,
            'subtitleFontSize': int
        }

        # Establecer valores predeterminados
        self.anchor = kwargs.get('anchor', 'start')  # start, middle, end, None
        self.color = kwargs.get('color', COLORS["text"])
        self.font = kwargs.get('font', FONT)
        self.fontSize = kwargs.get('fontSize', FONT_SIZES["lg"])
        self.fontWeight = kwargs.get('fontWeight', 'bold')  # bold lighter 100 200 900
        self.offset = kwargs.get('offset', SPACING["xl"])
        self.subtitleColor = kwargs.get('subtitleColor', COLORS["text"])
        self.subtitleFontSize = kwargs.get('subtitleFontSize', FONT_SIZES["md"])

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

    def create_title(self):
        new_title = Title(
            anchor=self.anchor,
            color=self.color,
            font=self.font,
            fontSize=self.fontSize,
            fontWeight=self.fontWeight,
            offset=self.offset,
            subtitleColor=self.subtitleColor,
            subtitleFontSize=self.subtitleFontSize
        )
        return new_title
