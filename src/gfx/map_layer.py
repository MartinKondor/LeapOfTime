"""
MapLayer class for storing class layers.
"""

class MapLayer:

    def __init__(self, layer, is_solid=None):
        self.layer = layer
        self.is_solid = False if is_solid is None else is_solid

    def __getitem__(self, key):
        return self.layer[key]

    def __iter__(self):
        return self.layer.__iter__()

    def __len__(self):
        return len(self.layer)

    def __str__(self):
        return str(self.layer)
