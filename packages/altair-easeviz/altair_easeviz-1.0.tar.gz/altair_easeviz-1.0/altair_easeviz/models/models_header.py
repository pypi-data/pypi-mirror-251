from altair_easeviz.tokens import FONT, FONT_SIZES, COLORS
from altair_easeviz.types_theme import Header


class HeaderModel():

    def __init__(self, **kwargs):
        self._required_params = {
            'labelColor': str,
            'labelFont': str,
            'labelFontSize': int,
            'titleColor': str,
            'titleFont': str,
            'titleFontSize': int
        }

        # Establecer valores predeterminados
        self.labelColor = kwargs.get('labelColor', COLORS["text"])
        self.labelFont = kwargs.get('labelFont', FONT)
        self.labelFontSize = kwargs.get('labelFontSize', FONT_SIZES["sm"])
        self.titleColor = kwargs.get('titleColor', COLORS["text"])
        self.titleFont = kwargs.get('titleFont', FONT)
        self.titleFontSize = kwargs.get('titleFontSize', FONT_SIZES["md"])

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

    def create_header(self):
        new_header = Header(
            labelColor=self.labelColor,
            labelFont=self.labelFont,
            labelFontSize=self.labelFontSize,
            titleColor=self.titleColor,
            titleFont=self.titleFont,
            titleFontSize=self.titleFontSize
        )

        return new_header
