from __future__ import annotations

from typing import Literal, Type

from grid import Grid
from resources import Aerofoam, Crystal, Iron, Oil
from thing import Thing
from tiles import Tile


class Building(Thing):
    name = "Building Baseclass"
    subdir = "buildings"

    _schematic: Grid = None

    BUILDING_REGISTRY: list[Type[Building]] = []

    @classmethod
    def __init_subclass__(cls, **kwargs):
        if cls._schematic:
            cls.BUILDING_REGISTRY.append(cls)  # Add class to registry.

    @classmethod
    def get_schematic(cls, rotation: Literal[0, 1, 2, 3] = 0) -> Grid:
        """Get the schematic with the desired rotation."""
        schematic = cls._schematic
        for _ in range(rotation):
            schematic.rotate()
        return schematic


def grid_from_transposed(schematic: list[list[Tile]]):
    transpose = [list(i) for i in zip(*schematic, strict=True)]
    return Grid(initial=transpose)


class Base(Building):
    name = "Base"


class WardenOutpost(Building):
    name = "Warden Outpost"
    schematic_list = [[Tile(Iron), Tile(Oil), Tile(Iron)], [Tile(), Tile(Aerofoam), Tile()]]
    _schematic = grid_from_transposed(schematic_list)


class CommsTower(Building):
    name = "Comms Tower"
    schematic_list = [[Tile(Crystal), Tile(Iron), Tile(Crystal), Tile(Oil)]]
    _schematic = grid_from_transposed(schematic_list)


class ArsenicScrubber(Building):
    name = "Arsenic Scrubber"
    schematic_list = [[Tile(), Tile(Crystal)], [Tile(), Tile(Oil)], [Tile(Aerofoam), Tile(Iron)]]
    _schematic = grid_from_transposed(schematic_list)
