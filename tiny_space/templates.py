from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, TypeVar, cast

import pygame as pg

from .helpers import Box, Point

class DummyAttribute:
    pass

R = TypeVar("R")


def abstract_attribute(obj: Callable[[Any], R] | None = None) -> R:
    _obj = cast(Any, obj)
    if obj is None:
        _obj = DummyAttribute()
    _obj.__is_abstract_attribute__ = True # type: ignore[reportAttributeAccessIssue]
    return cast(R, _obj)


class SurfaceInputComponent:
    """Generic surface component for handling user input."""

    @staticmethod
    def get_mouse_position(surface: Surface) -> Point:
        pos = Point(*pg.mouse.get_pos()).relative_to(surface.box)
        if pos is None:
            print("Error: Mouse has no position!")
            return Point(0, 0)
        return pos


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
