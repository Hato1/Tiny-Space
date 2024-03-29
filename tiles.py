"""
Holds the classes for the structures that are placed on the map
"""

from typing import Type

import pygame as pg

from buildings import Building
from resources import Resource

# import structures


class Tile:
    def __init__(self, is_empty: bool = True, contains: None | Type[Resource] | Type[Building] = None):
        self.name = "UNUSED"
        self.score = 0
        self.empty = is_empty
        self.contains = contains

    def draw_tile(self) -> pg.Surface:
        if self.contains:
            return self.contains.image()
        else:
            raise NotImplementedError
