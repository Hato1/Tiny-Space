"""
Handles the state of the cursor
"""

from enum import Enum
from typing import Type

from buildings import Building
from grid import Grid
from resources import Iron
from tiles import Tile


class CursorStates(Enum):
    RESOURCE_PLACE = 1
    BUILD_OUTLINE = 2
    BUILD_LOCATION = 3


class Cursor:
    def __init__(self):
        self._state: CursorStates = CursorStates.RESOURCE_PLACE
        self.selected_structure: Type[Building] | None = None

    def set_state(self, state: CursorStates):
        self._state = state

    def set_building(self, building: Type[Building]):
        self.selected_structure = building

    def get_state(self):
        return self._state

    def get_shape(self) -> Grid:
        if self._state == CursorStates.RESOURCE_PLACE:
            return Grid(initial=[[Tile(Iron)]])
        else:
            return self.selected_structure.get_schematic()

    def get_building(self):
        return self.selected_structure


cursor = Cursor()
