import logging

from .buildings import *
from .cursor import CursorStates, cursor


def debug_1():
    logging.warning("Debug 1")
    cursor.set_state(CursorStates.RESOURCE_PLACE)


def debug_2():
    logging.warning("Debug 2")
    if b := cursor.get_building():
        new_index = (Building.BUILDING_REGISTRY.index(b) + 1) % len(Building.BUILDING_REGISTRY)
        building = Building.BUILDING_REGISTRY[new_index]
    else:
        building = Building.BUILDING_REGISTRY[0]
    cursor.set_state(CursorStates.BUILD_OUTLINE, building=building)


def debug_3():
    logging.warning("Debug 3")
    cursor.rotate()
