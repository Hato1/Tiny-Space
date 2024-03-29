from __future__ import annotations

from pathlib import Path

import pygame as pg


class BuildingMeta(type):
    def __repr__(self):
        return self.__name__


class Building(metaclass=BuildingMeta):

    @classmethod
    def image(cls):
        return pg.image.load(cls.get_file)

    @classmethod
    def get_file(cls) -> Path:
        file = Path(f"assets/structures/{cls}.png")
        assert file.exists(), f"Could not find resource: {file!r}"
        return file


class Base(Building):
    pass
