"""
Holds the classes for the structures that are placed on the map
"""

from typing import Type

import pygame as pg

from buildings import Building
from resources import Resource

# import structures


class Tile:
    def __init__(self, contains: None | Type[Resource] | Type[Building] = None):
        self.name = "UNUSED"
        self.score = 0
        self.contains = contains

    @property
    def empty(self) -> bool:
        return type(self.contains) not in [type(Resource), type(Building)]

    @property
    def full(self) -> bool:
        return not self.empty

    def draw_tile(self) -> pg.Surface:
        if self.contains:
            return self.contains.image()
        else:
            raise NotImplementedError
