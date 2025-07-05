"""Definitions of building types.

Buildings are subclasses of Thing.
Buildings are 'built' from collections of resources according to their Schematic.
"""
from __future__ import annotations

from typing import Type

from tiny_space.helpers import add_spaces_to_camelcase

from .grid import Grid
from .resources import Aerofoam, Crystal, Iron, Oil
from .thing import Thing, Nothing
from .tiles import Tile


DUMMY_GRID = Grid()

class Building(Thing):
    # name = "Building Baseclass"
    asset_subdir = "buildings"

    _schematic: Grid = DUMMY_GRID

    BUILDING_REGISTRY: list[Type[Building]] = []

    score = 1

    @classmethod
    def __init_subclass__(cls, **kwargs):
        # Only register buildings with valid schematics.
        if cls._schematic is not DUMMY_GRID:
            cls.BUILDING_REGISTRY.append(cls)  # Add class to registry.

    @classmethod
    def get_schematic(cls, rotation: int = 0) -> Grid:
        """Get the schematic with the desired rotation."""
        return cls._schematic.rotate(rotation)
    
    @classmethod
    def get_name(cls) -> str:
        return add_spaces_to_camelcase(repr(cls))


def grid_from_transposed(schematic: list[list[Tile]]):
    transpose = [list(i) for i in zip(*schematic, strict=True)]
    return Grid(initial=transpose)


class Base(Building):
    ...

class WardenOutpost(Building):
    # schematic_list = [[Tile(Iron), Tile(Oil), Tile(Iron)], [Tile(Nothing), Tile(Aerofoam), Tile(Nothing)]]
    schematic_list = [[Tile(Oil), Tile(Crystal), Tile(Crystal)], [Tile(Nothing), Tile(Aerofoam), Tile(Nothing)]]
    _schematic = grid_from_transposed(schematic_list)
    score = 5


class CommsTower(Building):
    schematic_list = [[Tile(Crystal), Tile(Iron), Tile(Crystal), Tile(Oil)]]
    _schematic = grid_from_transposed(schematic_list)


class ArsenicScrubber(Building):
    schematic_list = [[Tile(Nothing), Tile(Crystal)], [Tile(Nothing), Tile(Oil)], [Tile(Aerofoam), Tile(Iron)]]
    _schematic = grid_from_transposed(schematic_list)
