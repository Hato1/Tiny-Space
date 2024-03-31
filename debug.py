import logging

from buildings import *
from cursor import CursorStates, cursor


def debug_1():
    logging.warning("Debug 1")
    cursor.set_state(CursorStates.RESOURCE_PLACE)


def debug_2():
    logging.warning("Debug 2")
    cursor.set_state(CursorStates.BUILD_OUTLINE)
    cursor.set_building(ArsenicScrubber)


def debug_3():
    logging.warning("Debug 3")
