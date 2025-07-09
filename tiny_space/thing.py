"""Definition of Thing.

A thing occupies a board tile. Buildings and resources subclass from Thing.
Thing classes are singletons.
"""

import logging
from functools import cache
from pathlib import Path

import pygame as pg


# Sneaky way to get the
class ThingMeta(type):
    def __repr__(self):
        return self.__name__


class Thing(metaclass=ThingMeta):
    """Base class representing the contents of a board tile.

    Board tiles can only contain one 'Thing' at a time.
    Things are all singletons, so they can be compared using their classname.
    Place the asset of a thing at "assets / cls.asset_subdir / class_name.png".
    """

    asset_subdir: str = ""
    score = 0

    @classmethod
    @cache
    def image(cls):
        return pg.image.load(cls.get_sprite_file())

    @classmethod
    def get_sprite_file(cls) -> Path:
        file = Path("assets") / cls.asset_subdir / f"{cls}.png"
        if not file.exists():
            logging.critical(f"Could not find resource: {file!r}")
            file = Path("assets") / "error.png"
        return file

    def __eq__(self, obj) -> bool:
        return repr(self) == repr(obj)


class Nothing:
    score = 0

    @classmethod
    def image(cls):
        return None


Tile = type[Thing] | type[Nothing]
