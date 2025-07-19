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
