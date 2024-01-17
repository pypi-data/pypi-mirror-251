from altair_easeviz.types_theme import View


class ViewModel():

    def __init__(self, **kwargs):
        self._required_params = {
            'continuousHeight': int,
            'continuousWidth': int,
            'stroke': str
        }

        # Establecer valores predeterminados
        self.continuousHeight = kwargs.get('continuousHeight', 300)
        self.continuousWidth = kwargs.get('continuousWidth', 400)
        self.stroke = kwargs.get('stroke', 'transparent')

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

    def create_view(self):
        new_view = View(
            continuousHeight=self.continuousHeight,
            continuousWidth=self.continuousWidth,
            stroke=self.stroke
        )
        return new_view
