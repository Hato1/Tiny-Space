"""

"""

import logging
from typing import Iterator, Type, overload

import pygame

from buildings import Base, Building
from helpers import ORTHOGONAL, GridPoint, Point
from resources import Queue, Resource
from templates import Surface
from tiles import Tile

common_colours = {"BLACK": (0, 0, 0), "WHITE": (200, 200, 200), "BLUE": (30, 30, 200)}


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

    def __init__(self, size: GridPoint):
        self.size: GridPoint = size
        self._grid: list[list[Tile]]
        self._initialise_grid()

    def _initialise_grid(self):
        """Set tiles to a 2d grid according to grid_size and place the Base structure in the center tile."""
        self._grid = [[Tile() for _ in range(self.size.y)] for _ in range(self.size.x)]
        self[self.size.x // 2, self.size.y // 2].contains = Base

    def is_in_grid(self, point: GridPoint) -> bool:
        """Return whether point lies in the grid"""
        return 0 <= point.x < self.size.x and 0 <= point.y < self.size.y

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
        for x in range(self.width):
            for y in range(self.height):
                yield GridPoint(x, y), self[x, y]


class RenderGrid(Surface):
    def process_inputs(self, mouse_position: Point):
        # This is handled by World
        pass

    def __init__(self, grid: Grid, cell_size):
        self.cell_size = cell_size
        self.grid = grid
        # Add an extra two pixels of padding to fit the lined border.
        # TODO: Draw the border on the outer canvas instead of on the grid.
        surface_size = Point(self.grid.width * self.cell_size + 2, self.grid.height * self.cell_size + 2)
        self.surface = pygame.Surface(surface_size)

    def get_name(self):
        return "Grid"

    def pixels_to_grid(self, point: Point) -> GridPoint:
        """Return Grid coordinate of point in pixels."""
        return GridPoint(int(point.x // self.cell_size), int(point.y // self.cell_size))

    def draw_grid_surface(self):
        """Draw the grid lines in the center of the display."""
        line_width = 2
        max_x, max_y = self.surface.get_size()
        for x in range(0, max_x, self.cell_size):
            pygame.draw.line(self.surface, common_colours["BLUE"], (x, 0), (x, max_y), line_width)

        for y in range(0, max_y, self.cell_size):
            pygame.draw.line(self.surface, common_colours["BLUE"], (0, y), (max_x, y), line_width)

        pygame.draw.line(self.surface, common_colours["BLUE"], (0, max_y), (max_x, max_y), line_width)
        pygame.draw.line(self.surface, common_colours["BLUE"], (max_x, 0), (max_x, max_y), line_width)

    def draw_tile(self, thing: Type[Resource] | Type[Building], grid_coord: GridPoint):
        asset_size = Point(*thing.image().get_size())
        self.surface.blit(
            thing.image(),
            (
                (grid_coord.x + 0.5) * self.cell_size - asset_size.x // 2,
                (grid_coord.y + 0.5) * self.cell_size - asset_size.y // 2,
            ),
        )

    def draw_tiles(self):
        for point, tile in self.grid:
            if thing := tile.contains:
                self.draw_tile(thing, point)

    def render(self) -> pygame.Surface:
        self.draw_grid_surface()
        self.draw_tiles()
        return self.surface


class World(Surface):
    default_grid_size = GridPoint(7, 7)

    def __init__(self, width: int, height: int, grid_size: GridPoint = default_grid_size, cell_size: int = 50):
        assert grid_size.x * cell_size < width, "Grid too wide for display area!"
        assert grid_size.y * cell_size < height, "Grid too tall for display area!"
        self.name = "World"
        self.grid = Grid(grid_size)
        self.render_grid = RenderGrid(self.grid, cell_size)
        self.world_surface = pygame.Surface((width, height))

    def get_name(self) -> str:
        return self.name

    def get_render_grid_rect(self):
        return self.render_grid.surface.get_rect(center=self.world_surface.get_rect().center)

    def process_inputs(self, mouse_position: Point):
        grid_coord = self.render_grid.pixels_to_grid(mouse_position - Point(*self.get_render_grid_rect()[:2]))
        # Fails if clicked elsewhere on the canvas.
        if self.grid.is_in_grid(grid_coord):
            resource = Queue.peek()
            if self.fill_tile(grid_coord, resource):
                Queue.take()

    def render(self) -> pygame.Surface:
        """Blit the grid to the center of the canvas."""
        self.world_surface.fill(common_colours["BLACK"])
        grid = self.render_grid.render()
        self.world_surface.blit(grid, self.get_render_grid_rect())
        return self.world_surface

    def has_adjacent_tile(self, grid_coord: GridPoint) -> bool:
        """Returns True if an adjacent tile isn't empty."""
        orthogonal_tiles: list[GridPoint] = [grid_coord + direction for direction in ORTHOGONAL]
        for point in orthogonal_tiles:
            if self.grid.is_in_grid(point) and not self.grid[point].empty:
                return True
        return False

    def fill_tile(self, point: GridPoint, thing: Type[Resource] | Type[Building]) -> bool:
        """Fill the tile, if possible.

        Filling a tile is not possible if it's already filled or if there are no adjacent filled tiles.
        """
        if self.grid[point].full:
            logging.warning(f"Illegal move: Can't fill occupied tile at {point}.")
            return False
        if not self.has_adjacent_tile(point):
            logging.warning(f"Illegal move: Can't fill disconnected tile at {point}.")
            return False
        self.grid[point].contains = thing
        return True
