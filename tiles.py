"""
Holds the classes for the structures that are placed on the map
"""


class Tile:
    def __init__(self):
        self.name = "UNUSED"
        self.score = 0
        self.world_location = (0, 0)
        self.screen_location = (0, 0)
        self.empty = True


class EmptyTile(Tile):
    def __init__(self):
        super().__init__()
        self.name = "Empty"


class Base(Tile):
    def __init__(self):
        super().__init__()
        self.name = "Base"
        self.empty = False


class Resource(Tile):
    def __init__(self):
        super().__init__()
        self.score = 1
        self.empty = False


class Structure(Tile):
    def __init__(self):
        super().__init__()
        self.score = 3
        self.empty = False
