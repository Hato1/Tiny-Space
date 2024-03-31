import logging

from buildings import *
from cursor import CursorStates, cursor


def debug_1():
    logging.warning("Debug 1")
    cursor.set_state(CursorStates.RESOURCE_PLACE)
    cursor.set_building(None)


def debug_2():
    logging.warning("Debug 2")
    cursor.set_state(CursorStates.BUILD_OUTLINE)
    if b := cursor.get_building():
        new_index = (Building.BUILDING_REGISTRY.index(b) + 1) % len(Building.BUILDING_REGISTRY)
        cursor.set_building(Building.BUILDING_REGISTRY[new_index])
    else:
        cursor.set_building(Building.BUILDING_REGISTRY[0])


def debug_3():
    logging.warning("Debug 3")
