from altair_easeviz.models.models_axis import AxisModel
from altair_easeviz.models.models_header import HeaderModel
from altair_easeviz.models.models_legend import LegendModel
from altair_easeviz.models.models_range import RangeModel
from altair_easeviz.models.models_title import TitleModel
from altair_easeviz.models.models_view import ViewModel
from altair_easeviz.types_theme import Config, Axis, Legend, ScaleRange, Header, Title, View


class ConfigModel:

    def __init__(self, **kwargs):
        self._required_params = {
            'axis': Axis,
            'legend': Legend,
            'range': ScaleRange,
            'background': str,
            'header': Header,
            'title': Title,
            'view': View
        }

        # Establecer valores predeterminados
        self.axis = kwargs.get('axis', AxisModel().create_axis())
        self.legend = kwargs.get('legend', LegendModel().create_legend())
        self.range = kwargs.get('range', RangeModel().create_range())
        self.background = kwargs.get('background', '#FFFFFF')
        self.header = kwargs.get('header', HeaderModel().create_header())
        self.title = kwargs.get('title', TitleModel().create_title())
        self.view = kwargs.get('view', ViewModel().create_view())

        # Actualizar atributos con kwargs
        self.__dict__.update(kwargs)

        '''# Verificar tipos de datos para los parámetros obligatorios
        for param, expected_type in self._required_params.items():
            if param in kwargs and not isinstance(getattr(self, param), expected_type):
                raise TypeError(f"Se esperaba '{param}' como tipo {expected_type}.")
        '''
        # Verificar que los parámetros obligatorios tengan valores
        missing_params = [param for param, expected_type in self._required_params.items() if
                          getattr(self, param, None) is None]
        if missing_params:
            raise ValueError(
                f"Los siguientes parámetros son obligatorios y no fueron proporcionados: {missing_params}")

    def create_config(self):
        new_config = {'config': Config(
            axis=self.axis,
            legend=self.legend,
            range=self.range,
            background=self.background,
            header=self.header,
            title=self.title,
            view=self.view
        )}
        return new_config

    def create_full_config(self):
        """
        This configuration return all parameters inserted when the class was created, make sure the parameters entered,
        are the same as described in vega-altair altair.Config
        :return (dict): A dictioanry with all the configuration ready to register and enable
        """
        result_dict = self.__dict__.copy()
        result_dict.pop('_required_params', None)
        return {"config": result_dict}

    def __str__(self):
        return str(self.create_full_config())
