from typing import List

from altair_easeviz.tokens import COLORS
from altair_easeviz.types_theme import ScaleRange


class RangeModel():

    def __init__(self, **kwargs):
        # Establecer valores predeterminados
        self.category = kwargs.get('category', COLORS["schemes"]["categorical"]["dark2"])
        self.diverging = kwargs.get('diverging', COLORS["schemes"]["diverging"]["bluered"])
        self.heatmap = kwargs.get('heatmap', COLORS["schemes"]["sequential"]["blues"])
        self.ramp = kwargs.get('ramp', COLORS["schemes"]["sequential"]["blues"])

        # Actualizar atributos con kwargs
        self.__dict__.update(kwargs)

    def create_range(self):
        new_range = ScaleRange(
            category=self.category,
            diverging=self.diverging,
            heatmap=self.heatmap,
            ramp=self.ramp
        )
        return new_range
