from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, TypeVar, cast

import pygame as pg

from .helpers import Point


class DummyAttribute:
    pass


R = TypeVar("R")


def abstract_attribute(obj: Callable[[Any], R] | None = None) -> R:
    _obj = cast(Any, obj)
    if obj is None:
        _obj = DummyAttribute()
    _obj.__is_abstract_attribute__ = True  # type: ignore[reportAttributeAccessIssue,unused-ignore]
    return cast(R, _obj)


# class SurfaceInputComponent:
#     """Generic surface component for handling user input."""

#     @staticmethod
#     def get_mouse_position(surface: GraphicsComponent) -> Point:
#         pos = Point(*pg.mouse.get_pos()).relative_to(surface.surface.get_rect())
#         if pos is None:
#             logging.error("Error: Mouse has no position!")
#             return Point(0, 0)
#         return pos


# class Surface(pg.Surface):
#     def __init__(self, box: pg.Rect, *args, **kwargs):
#         self.position = box.topleft
#         super().__init__(box.size, *args, **kwargs)

#     def get_rect(self, **kwargs) -> pg.Rect:
#         rect = super().get_rect(**kwargs)
#         return pg.Rect(*self.position, *rect.bottomright)


class GraphicsComponent(ABC):
    @property
    def name(self):
        return type(self).__name__

    @abstract_attribute
    def surface(self) -> pg.Surface:
        raise NotImplementedError

    @abstractmethod
    def render(self, *args, **kwargs) -> pg.Surface:
        raise NotImplementedError

    def update(self) -> None:  # noqa: B027
        """Update game for 1 frame."""
        pass

    def process_inputs(self, mouse_position: Point):  # noqa: B027
        raise NotImplementedError
