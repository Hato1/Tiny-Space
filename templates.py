from __future__ import annotations

from abc import ABC, abstractmethod

import pygame as pg

from helpers import Box, Point, abstract_attribute


class SurfaceInputComponent:
    """Generic surface component for handling user input."""

    @staticmethod
    def get_mouse_position(surface: Surface) -> Point:
        return Point(*pg.mouse.get_pos()).relative_to(surface.box)


class Surface(ABC):
    @property
    def name(self):
        assert hasattr(self, "__name__")
        return self.__name__

    @abstract_attribute
    def box(self) -> Box:
        raise NotImplementedError

    @abstractmethod
    def render(self, *args, **kwargs) -> pg.Surface:
        raise NotImplementedError

    def update(self) -> None:  # noqa: B027
        """Update game for 1 frame."""
        pass

    def process_inputs(self, mouse_position: Point):  # noqa: B027
        raise NotImplementedError
