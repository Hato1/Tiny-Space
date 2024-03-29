"""
Handles the state of the cursor
"""

from enum import Enum


class CursorStates(Enum):
    RESOURCE_PLACE = 1
    BUILD_OUTLINE = 2
    BUILD_LOCATION = 3


class Cursor:
    def __init__(self):
        self._state = CursorStates.RESOURCE_PLACE

    def set_state(self, state: CursorStates):
        self._state = state

    def get_state(self):
        return self._state


cursor = Cursor()
