from __future__ import annotations

from typing import Iterator, overload

from .helpers import GridPoint, Point
from .tiles import Tile


class Grid:
    """Low level generic object representing a 2d grid that can be treated similarly to a list of lists.

    As a rule of thumb, it shouldn't contain any logic specific to the game.

    You can index into the grid like so:
    g = Grid()
    g[3,4]

    You can iterate through all tiles in the grid like this:
    g = Grid()
    for point, tile in g:
        assert g[point] == tile

    Methods:
        is_in_grid(self, point: GridPoint) -> bool
        height(self) -> int
        width(self) -> int
    """

    def __init__(self, size: GridPoint | None = None, initial: list[list[Tile]] | None = None):
        self._grid: list[list[Tile]]
        if initial:
            self._grid = initial
        else:
            self._initialise_grid(size)

    def __eq__(self, other):
        if not isinstance(other, Grid):
            return False
        return not any(
            pos1 != pos2 or tile1.contains != tile2.contains
            for (pos1, tile1), (pos2, tile2) in zip(self, other, strict=True)
        )

    def __repr__(self):
        string = "[["
        row_count = 0
        for pos, item in self:
            if pos.y != row_count:
                row_count = pos.y
                string = f"{string[:-2]}], ["
            string += f"{item.contains}, "
        return f"{string[:-2]}]]"

    @property
    def size(self):
        return Point(len(self._grid), len(self._grid[0]))

    def _initialise_grid(self, size):
        """Set tiles to a 2d grid according to grid_size and place the Base structure in the center tile."""
        self._grid = [[Tile() for _ in range(size.y)] for _ in range(size.x)]

    def is_in_grid(self, point: GridPoint) -> bool:
        """Return whether point lies in the grid"""
        return 0 <= point.x < self.size.x and 0 <= point.y < self.size.y

    def get_subgrid(self, x, y, width, height) -> tuple[Grid, GridPoint]:
        """Return a Grid consisting of a subgrid of self"""
        sub_list = [column[y:y+height] for column in self._grid[x:x+width]]
        subgrid = Grid(initial=sub_list[:])
        assert subgrid.size == Point(width, height), f"{subgrid.size} is not equal to {Point(width, height)}!"
        return subgrid, GridPoint(x, y)

    @property
    def height(self) -> int:
        """Get the number of rows"""
        return self.size.y

    @property
    def width(self) -> int:
        """Get the number of cols"""
        return self.size.x

    @overload
    def __getitem__(self, index: int) -> list[Tile]: ...

    @overload
    def __getitem__(self, index: tuple | GridPoint) -> Tile: ...

    def __getitem__(self, index: int | tuple) -> list[Tile] | Tile:
        """Retrieve elements of the map at the given row or (row, col) pair"""
        if isinstance(index, int):
            return self._grid[index]
        elif isinstance(index, (tuple, GridPoint)):
            index = GridPoint(*index)
            return self._grid[index.x][index.y]
        raise ValueError

    def __iter__(self) -> Iterator[tuple[GridPoint, Tile]]:
        for y in range(self.height):
            for x in range(self.width):
                yield GridPoint(x, y), self[x, y]

    def rotate(self, times: int) -> Grid:
        """Rotate by 90 degrees n times."""
        grid: list[list[Tile]] = self._grid
        for _ in range(times):
            grid = list(zip(*grid[::-1], strict=True))  # type: ignore[arg-type]
        return Grid(initial=grid)
