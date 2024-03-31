from pathlib import Path

import pygame as pg


class ThingMeta(type):
    def __repr__(self):
        return self.__name__


class Thing(metaclass=ThingMeta):
    subdir: str = ""

    @classmethod
    def image(cls):
        return pg.image.load(cls.get_file())

    @classmethod
    def get_file(cls) -> Path:
        file = Path("assets") / cls.subdir / f"{cls}.png"
        assert file.exists(), f"Could not find resource: {file!r}"
        return file
