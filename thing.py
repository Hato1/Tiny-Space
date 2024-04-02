import logging
from pathlib import Path

import pygame as pg


class ThingMeta(type):
    def __repr__(self):
        return self.__name__


class Thing(metaclass=ThingMeta):
    subdir: str = ""
    file: Path | None = None
    score = 0

    @classmethod
    def image(cls):
        return pg.image.load(cls.get_file())

    @classmethod
    def get_file(cls) -> Path:
        if cls.file:
            return cls.file
        file = Path("assets") / cls.subdir / f"{cls}.png"
        if not file.exists():
            logging.critical(f"Could not find resource: {file!r}")
            file = Path("assets") / "error.png"
        cls.file = file
        return file
