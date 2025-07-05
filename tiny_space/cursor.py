"""
Handles the state of the cursor
"""

from enum import Enum
from typing import Type

from .buildings import Building
from .grid import Grid
from .helpers import GridPoint
from .resources import Resource


class CursorStates(Enum):
    RESOURCE_PLACE = 1
    BUILD_OUTLINE = 2
    BUILD_LOCATION = 3


class Cursor:
    def __init__(self):
        self._state: CursorStates = CursorStates.RESOURCE_PLACE
        self.rotation: int = 0
        self.selected_structure: Type[Building] | None = None
        self.shadow_location: GridPoint | None = None
        # The grid coordinate is the mouse is currently over.
        self.moused_tile: GridPoint | None = None

    def set_state(self, state: CursorStates, **kwargs):
        if state is CursorStates.RESOURCE_PLACE:
            self.shadow_location = None
            self.selected_structure = None
        if state is CursorStates.BUILD_OUTLINE:
            self.selected_structure = kwargs["building"]
            self.shadow_location = None
            self.rotation = 0
        if state is CursorStates.BUILD_LOCATION:
            assert self.selected_structure, "Tried to skip cursor state BUILD_OUTLINE."
            self.shadow_location = kwargs["location"]
        self._state = state

    def rotate(self):
        self.rotation = (self.rotation + 1) % 4

    def get_state(self):
        return self._state

    def get_building_location(self):
        return self.shadow_location

    def get_shape(self) -> Grid:
        if self._state in [CursorStates.RESOURCE_PLACE, CursorStates.BUILD_LOCATION]:
            return Grid([[Resource]])

        assert self.selected_structure
        return self.selected_structure.get_schematic(self.rotation)

    def get_shadow_shape(self) -> Grid | None:
        if self._state is not CursorStates.BUILD_LOCATION:
            return None
        assert self.selected_structure
        return self.selected_structure.get_schematic(self.rotation)

    def get_building(self) -> type[Building] | None:
        return self.selected_structure


cursor = Cursor()
