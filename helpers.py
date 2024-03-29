from __future__ import annotations

from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int

    def relative_to(self, box: Box):
        return Point(self.x - box.x, self.y - box.y)


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
        if self.x < point.x < self.max_x:
            if self.y < point.y < self.max_y:
                return True
        return False
