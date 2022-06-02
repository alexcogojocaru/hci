import json


PRIMARY = 'primary'
SECONDARY = 'secondary'
EXTRA = 'extra'

class ColorConfig:
    def __init__(self, path) -> None:
        with open(path, 'r') as fo:
            self._colors = json.load(fo)

    @property
    def primary_color(self):
        return self._colors[PRIMARY]
    
    @property
    def secondary_color(self):
        return self._colors[SECONDARY]
    
    @property
    def extra_color(self):
        return self._colors[EXTRA]
