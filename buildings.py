from __future__ import annotations

from typing import Type

from grid import Grid
from resources import Aerofoam, Crystal, Iron, Oil
from thing import Thing
from tiles import Null, Tile


class Building(Thing):
    name = "Building Baseclass"
    subdir = "buildings"

    _schematic: Grid = None

    BUILDING_REGISTRY: list[Type[Building]] = []

    score = 1

    @classmethod
    def __init_subclass__(cls, **kwargs):
        if cls._schematic:
            cls.BUILDING_REGISTRY.append(cls)  # Add class to registry.

    @classmethod
    def get_schematic(cls, rotation: int = 0) -> Grid:
        """Get the schematic with the desired rotation."""
        return cls._schematic.rotate(rotation)


def grid_from_transposed(schematic: list[list[Tile]]):
    transpose = [list(i) for i in zip(*schematic, strict=True)]
    return Grid(initial=transpose)


class Base(Building):
    name = "Base"


class WardenOutpost(Building):
    name = "Warden Outpost"
    # schematic_list = [[Tile(Iron), Tile(Oil), Tile(Iron)], [Null(), Tile(Aerofoam), Null()]]
    schematic_list = [[Tile(Oil), Tile(Crystal), Tile(Crystal)], [Null(), Tile(Aerofoam), Null()]]
    _schematic = grid_from_transposed(schematic_list)
    score = 5


class CommsTower(Building):
    name = "Comms Tower"
    schematic_list = [[Tile(Crystal), Tile(Iron), Tile(Crystal), Tile(Oil)]]
    _schematic = grid_from_transposed(schematic_list)


class ArsenicScrubber(Building):
    name = "Arsenic Scrubber"
    schematic_list = [[Null(), Tile(Crystal)], [Null(), Tile(Oil)], [Tile(Aerofoam), Tile(Iron)]]
    _schematic = grid_from_transposed(schematic_list)
