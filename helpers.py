from __future__ import annotations

from typing import NamedTuple, Self


class Point(NamedTuple):
    x: int
    y: int

    def relative_to(self, box: Box) -> Self:
        return self.__class__(self.x - box.x, self.y - box.y)

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

    def __repr__(self):
        return f"({self.x}, {self.y})"


class GridPoint(Point): ...


# Movement vectors
LEFT = GridPoint(1, 0)
RIGHT = GridPoint(-1, 0)
DOWN = GridPoint(0, 1)
UP = GridPoint(0, -1)

ORTHOGONAL = [LEFT, RIGHT, DOWN, UP]


class Box(NamedTuple):
    x: int
    y: int
    width: int
    height: int

    @property
    def max_x(self):
        return self.x + self.width

    @property
    def max_y(self):
        return self.y + self.height

    def contains(self, point: Point) -> bool:
        if self.x < point.x < self.max_x and self.y < point.y < self.max_y:
            return True
        return False


def handle_mouse_collision(surfaces, mouse_position: Point):
    for surface in surfaces:
        if surface.rect.collidepoint(mouse_position):
            # ToDo: Add subtract method to Point.
            relative_mouse_position = Point(mouse_position.x - surface.rect.x, mouse_position.y - surface.rect.y)
            surface.collision(relative_mouse_position)


class classproperty(property):
    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)
