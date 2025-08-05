"""Definitions of building types.

Buildings are subclasses of Thing.
Buildings are 'built' from collections of resources according to their Schematic.
"""

from __future__ import annotations

from typing import Type

from tiny_space.grid import Grid
from tiny_space.helpers import add_spaces_to_camelcase
from tiny_space.resources import Aerofoam, Crystal, Iron, Oil
from tiny_space.thing import Nothing, Thing, Tile


class Building(Thing):
    asset_subdir = "buildings"
    description = "I'm a building"

    # The 'recipe' to construct this building.
    _schematic: Grid | None = None

    BUILDING_REGISTRY: list[Type[Building]] = []

    @classmethod
    def __init_subclass__(cls, **kwargs):
        cls.BUILDING_REGISTRY.append(cls)  # Add class to registry.

    @classmethod
    def is_buildable(cls) -> bool:
        return cls._schematic is not None

    @classmethod
    def get_schematic(cls, rotation: int = 0) -> Grid:
        """Get the schematic rotated by 90 degrees n times."""
        if not cls._schematic:
            raise ValueError(f"No schematic for {repr(cls)}")
        return cls._schematic.rotate(rotation)

    @classmethod
    def get_name(cls) -> str:
        return add_spaces_to_camelcase(repr(cls))


def grid_from_transposed(schematic: list[list[Tile]]):
    """Transform a list of rows into a grid."""
    transpose = [list(i) for i in zip(*schematic, strict=True)]
    return Grid(transpose)


class Base(Building): ...


class WardenOutpost(Building):
    description = "Gives 2 points for each adjacent Facility."
    # schematic_list = [[Tile(Iron), Tile(Oil), Tile(Iron)], [Tile(Nothing), Tile(Aerofoam), Tile(Nothing)]]
    schematic_list: list[list[Tile]] = [[Oil, Crystal, Crystal], [Nothing, Aerofoam, Nothing]]
    _schematic = grid_from_transposed(schematic_list)
    score = 5


class CommsTower(Building):
    description = "aa a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a"
    schematic_list: list[list[Tile]] = [[Crystal, Iron, Crystal, Oil]]
    _schematic = grid_from_transposed(schematic_list)


class ArsenicScrubber(Building):
    schematic_list: list[list[Tile]] = [[Nothing, Crystal], [Nothing, Oil], [Aerofoam, Iron]]
    _schematic = grid_from_transposed(schematic_list)


class Lorem(Building):
    schematic_list: list[list[Tile]] = [[Nothing, Crystal], [Nothing, Oil], [Aerofoam, Iron]]
    _schematic = grid_from_transposed(schematic_list)


class Ipsum(Building):
    schematic_list: list[list[Tile]] = [[Nothing, Crystal], [Nothing, Oil], [Aerofoam, Iron]]
    _schematic = grid_from_transposed(schematic_list)


class Dolor(Building):
    schematic_list: list[list[Tile]] = [[Crystal], [Iron]]
    _schematic = grid_from_transposed(schematic_list)


class Sit(Building):
    schematic_list: list[list[Tile]] = [[Aerofoam, Oil]]
    _schematic = grid_from_transposed(schematic_list)


class Amet(Building):
    schematic_list: list[list[Tile]] = [[Oil]]
    _schematic = grid_from_transposed(schematic_list)
