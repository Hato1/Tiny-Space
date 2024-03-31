from __future__ import annotations

from pathlib import Path

import pygame as pg

from grid import Grid
from helpers import GridPoint
from resources import Aerofoam, Iron, Oil
from thing import Thing
from tiles import Tile


class Building(Thing):
    subdir = "buildings"

    schematic: Grid = None


def grid_from_transposed(schematic: list[list[Thing]]):
    transpose = [list(i) for i in zip(*schematic)]
    return Grid(initial=transpose)


class Base(Building):
    pass


class WardenOutpost(Building):
    schematic_list = [[Tile(Iron), Tile(Oil), Tile(Iron)], [Tile(), Tile(Aerofoam), Tile()]]

    schematic = grid_from_transposed(schematic_list)
