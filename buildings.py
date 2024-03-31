from __future__ import annotations

from typing import Type

from grid import Grid
from resources import Aerofoam, Crystal, Iron, Oil
from thing import Thing
from tiles import Tile


class Building(Thing):
    name = "Nonetype"
    subdir = "buildings"

    schematic: Grid = None

    BUILDING_REGISTRY: list[Type[Building]] = []

    @classmethod
    def __init_subclass__(cls, **kwargs):
        cls.BUILDING_REGISTRY.append(cls)  # Add class to registry.


def grid_from_transposed(schematic: list[list[Tile]]):
    transpose = [list(i) for i in zip(*schematic, strict=True)]
    return Grid(initial=transpose)


class Base(Building):
    name = "Base"


class WardenOutpost(Building):
    name = "Warden Outpost"
    schematic_list = [[Tile(Iron), Tile(Oil), Tile(Iron)], [Tile(), Tile(Aerofoam), Tile()]]
    schematic = grid_from_transposed(schematic_list)


class CommsTower(Building):
    name = "Comms Tower"
    schematic_list = [[Tile(Crystal), Tile(Iron), Tile(Crystal), Tile(Oil)]]
    schematic = grid_from_transposed(schematic_list)


class ArsenicScrubber(Building):
    name = "Arsenic Scrubber"
    schematic_list = [[Tile(), Tile(Crystal)], [Tile(), Tile(Oil)], [Tile(Aerofoam), Tile(Iron)]]
    schematic = grid_from_transposed(schematic_list)
