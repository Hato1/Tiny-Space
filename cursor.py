"""
Handles the state of the cursor
"""

from enum import Enum

from buildings import Building


class CursorStates(Enum):
    RESOURCE_PLACE = 1
    BUILD_OUTLINE = 2
    BUILD_LOCATION = 3


class Cursor:
    def __init__(self):
        self._state: CursorStates = CursorStates.RESOURCE_PLACE
        self._selected_structure: type[Building] = None

    def set_state(self, state: CursorStates):
        self._state = state

    def set_building(self, building: type[Building]):
        self._selected_structure = building

    def get_state(self):
        return self._state

    def get_building(self):
        return self._selected_structure


cursor = Cursor()
