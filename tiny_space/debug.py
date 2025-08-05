import logging

from tiny_space.buildings import Building
from tiny_space.cursor import CursorStates, cursor


def debug_1():
    logging.warning("Debug 1")
    cursor.set_state(CursorStates.RESOURCE_PLACE)


def debug_2():
    logging.warning("Debug 2")
    building_registry = [b for b in Building.BUILDING_REGISTRY if b.is_buildable()]
    if b := cursor.get_building():
        new_index = (building_registry.index(b) + 1) % len(building_registry)
        building = building_registry[new_index]
    else:
        building = building_registry[0]
    cursor.set_state(CursorStates.BUILD_OUTLINE, building=building)


def debug_3():
    logging.warning("Debug 3")
    cursor.rotate()
