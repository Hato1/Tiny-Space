from __future__ import annotations

from grid import Grid
from resources import Aerofoam, Iron, Oil
from thing import Thing
from tiles import Tile


class Building(Thing):
    name = "Nonetype"
    subdir = "buildings"

    schematic: Grid = None


def grid_from_transposed(schematic: list[list[Tile]]):
    transpose = [list(i) for i in zip(*schematic, strict=True)]
    return Grid(initial=transpose)


class Base(Building):
    name = "Base"
    pass


class WardenOutpost(Building):
    name = "Warden Outpost"
    schematic_list = [[Tile(Iron), Tile(Oil), Tile(Iron)], [Tile(), Tile(Aerofoam), Tile()]]

    schematic = grid_from_transposed(schematic_list)
