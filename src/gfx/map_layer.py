"""
MapLayer class for storing class layers.
"""

class MapLayer:

    def __init__(self, layer: list, is_solid: bool=None):
        self.layer = tuple(tuple(row) for row in layer)
        self.is_solid = False if is_solid is None else is_solid

    def __getitem__(self, key: int):
        return self.layer[key]

    def __iter__(self):
        return self.layer.__iter__()

    def __len__(self):
        return len(self.layer)

    def __str__(self):
        return ('*' if self.is_solid else '') + str(self.layer)
