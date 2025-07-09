from __future__ import annotations

from typing import Iterator, overload

from tiny_space.thing import Nothing, Tile

from .helpers import GridPoint


class Grid:
    """Low level generic object representing a 2d grid that can be treated similarly to a list of lists.

    Created to resolve confusion between X, Y, Width, Height, Rows, Columns. Additionally has methods for
    iteration and rotation.

    Try avoid any logic specific to the game for compatibility with other projects.

    You can index similarly to a real list[list[object]]
    g = Grid([
        [Iron, Oil],
        [Wood, Food].
    ])
    g[1,1]
    > Food
    g[0, 1] = Alice
    g[0]
    > [Iron, Alice]

    You can iterate through all tiles in the grid like this:
    g = Grid(...)
    for point, tile in g:
        assert g[point] == tile

    Methods:
        from_dimensions(size) -> Grid
        is_in_grid(point: GridPoint) -> bool
        height() -> int
        width() -> int
        rotate(n) -> Rotated copy of Grid
    """

    def __init__(self, initial: list[list[Tile]]):
        self._grid = initial

    @classmethod
    def from_dimensions(cls, size: GridPoint):
        """Make a grid of Nothing objects of the given dimensions."""
        return cls([[Nothing for _ in range(size.y)] for _ in range(size.x)])

    def __eq__(self, other):
        if not isinstance(other, Grid):
            return False
        return not any(pos1 != pos2 or tile1 != tile2 for (pos1, tile1), (pos2, tile2) in zip(self, other, strict=True))

    def __repr__(self):
        string = "[["
        row_count = 0
        for pos, item in self:
            if pos.y != row_count:
                row_count = pos.y
                string = f"{string[:-2]}], ["
            string += f"{item}, "
        return f"{string[:-2]}]]"

    @property
    def size(self):
        return GridPoint(len(self._grid), len(self._grid[0]))

    def is_in_grid(self, point: GridPoint) -> bool:
        """Return whether point lies in the grid"""
        return 0 <= point.x < self.size.x and 0 <= point.y < self.size.y

    def get_subgrid(self, x, y, width, height) -> tuple[Grid, GridPoint]:
        """Return a Grid consisting of a subgrid of self"""
        # TODO: Clean this up.
        sub_list = [column[y : y + height] for column in self._grid[x : x + width]]
        subgrid = Grid(sub_list[:])
        assert subgrid.size == GridPoint(width, height), f"{subgrid.size} is not equal to {GridPoint(width, height)}!"
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

    def __setitem__(self, index: GridPoint, value: Tile):
        self._grid[index.x][index.y] = value

    def __iter__(self) -> Iterator[tuple[GridPoint, Tile]]:
        for y in range(self.height):
            for x in range(self.width):
                yield GridPoint(x, y), self[x, y]

    def rotate(self, times: int) -> Grid:
        """Get a copy of this grid rotated by 90 degrees n times."""
        grid: list[list[Tile]] = self._grid
        for _ in range(times):
            grid = list(zip(*grid[::-1], strict=True))  # type: ignore[arg-type]
        return Grid(grid)
