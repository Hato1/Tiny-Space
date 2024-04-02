"""
Handles the state of the cursor
"""

from enum import Enum
from typing import Type

from buildings import Building
from grid import Grid
from helpers import GridPoint
from resources import Iron
from tiles import Tile


class CursorStates(Enum):
    RESOURCE_PLACE = 1
    BUILD_OUTLINE = 2
    BUILD_LOCATION = 3


class Cursor:
    def __init__(self):
        self._state: CursorStates = CursorStates.RESOURCE_PLACE
        self.rotation: int = 0
        self.selected_structure: Type[Building] | None = None
        self.building_location: GridPoint = None

    def set_state(self, state: CursorStates):
        self._state = state

    def set_building(self, building: Type[Building]):
        self.selected_structure = building
        self.rotation = 0

    def set_building_location(self, building_location: GridPoint):
        self.building_location = building_location

    def rotate(self):
        self.rotation = (self.rotation + 1) % 4

    def get_state(self):
        return self._state

    def get_building_location(self):
        return self.building_location

    def get_shape(self) -> Grid:
        if self._state == CursorStates.RESOURCE_PLACE:
            return Grid(initial=[[Tile(Iron)]])
        else:
            return self.selected_structure.get_schematic(self.rotation)

    def get_building(self):
        return self.selected_structure


cursor = Cursor()
