from __future__ import annotations

import re
from abc import ABC, abstractmethod
from enum import Enum
from typing import NamedTuple, Self


class Point(NamedTuple):
    """A class representing a point with x and y coordinates.

    Methods:
    - relative_to: Returns a new Point object that is relative to a given Box object.
    - __add__: Adds two Point objects or a Point object and a tuple.
    - __sub__: Subtracts two Point objects or a Point object and a tuple.
    - __mul__: Multiplies the Point object by a scalar.

    Attributes:
    - x: The x-coordinate of the point.
    - y: The y-coordinate of the point.

    Examples:
        p1 = Point(1, 2)
        p2 = Point(3, 4)
        p3 = p1 + p2
        # Output: P3=(4, 6)
    """

    x: int
    y: int

    def __add__(self, other: Point | tuple) -> Self:
        if isinstance(other, Point):
            return self.__class__(self.x + other[0], self.y + other[1])
        return NotImplemented

    def __sub__(self, other: Point | tuple) -> Self:
        if isinstance(other, Point):
            return self.__class__(self.x - other[0], self.y - other[1])
        return NotImplemented

    def __mul__(self, other: int) -> Self:  # type: ignore[override]
        """Multiply vector by a scalar"""
        return self.__class__(self.x * other, self.y * other)

    def __floordiv__(self, other: int) -> Self:
        """Multiply vector by a scalar"""
        return self.__class__(self.x // other, self.y // other)

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        raise NotImplementedError(f"Comparing Point with {type(other)}")


class GridPoint(Point):
    """A point lying on the game-grid board.

    Used to clarify when a point is in the pixel grid
    or the game grid.

    TODO: Test that typehinting/mypy complains when
    using one class to a function requesting the other.
    """


# Movement vectors
LEFT = GridPoint(-1, 0)
RIGHT = GridPoint(1, 0)
DOWN = GridPoint(0, 1)
UP = GridPoint(0, -1)

ORTHOGONAL = [LEFT, RIGHT, DOWN, UP]


class Event(Enum):
    """Event types to be sent via Notifier."""

    PlaceResource = 1
    PlaceBuilding = 2


class Notifier:
    """A simple Observer pattern implementation.

    Objects can be subclassed from Observer
    """

    # List of subscribers.
    _observers: list[Observer] = []

    @classmethod
    def attach(cls, observer: Observer) -> None:
        cls._observers.append(observer)

    @classmethod
    def detach(cls, observer: Observer) -> None:
        cls._observers.remove(observer)

    @classmethod
    def notify(cls, event: Event) -> None:
        """
        Trigger an update in each subscriber.
        """
        for observer in cls._observers:
            observer.event_listener(event)


class Observer(ABC):
    """Subclass from Observer to receive events."""

    def __init__(self, **kwargs):
        Notifier.attach(self)
        super().__init__(**kwargs)

    @abstractmethod
    def event_listener(self, event: Event) -> None:
        """
        Receive update from subject.
        """
        raise NotImplementedError


def add_spaces_to_camelcase(text: str) -> str:
    """Adds spaces to a camel case string.

    Handles cases like 'camelCase' to 'camel Case' and 'IBMCorp' to 'IBM Corp'.
    """
    # Insert a space before an uppercase letter that is not at the beginning
    # and is followed by a lowercase letter, or is preceded by a lowercase letter.
    s1 = re.sub(r"([A-Z])([A-Z][a-z])", r"\1 \2", text)
    # Insert a space before an uppercase letter that is preceded by a lowercase letter.
    return re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", s1)
