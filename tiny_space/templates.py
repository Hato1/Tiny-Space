from __future__ import annotations

import logging
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

    def update(self, time_delta: float) -> None:  # noqa: B027
        """Update game."""
        pass

    def process_inputs(self, mouse_position: Point):  # noqa: B027
        logging.warning("Mouse click not implemented for this grapihc component.")

    @staticmethod
    def process_inputs_subsurfaces(mouse_position: Point, surfaces: list[tuple[Point, GraphicsComponent]]):
        for pos, surface in surfaces:
            relative_position = mouse_position - pos
            if surface.surface.get_rect().collidepoint(relative_position):
                surface.process_inputs(mouse_position=relative_position)
