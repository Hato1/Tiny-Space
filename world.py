"""

"""

from __future__ import annotations

import logging
from typing import Iterator, Type, overload

import pygame

from buildings import Base, Building, WardenOutpost
from grid import Grid
from helpers import ORTHOGONAL, GridPoint, Point
from resources import Queue, Resource
from templates import Surface
from tiles import Tile

common_colours = {"BLACK": (0, 0, 0), "WHITE": (200, 200, 200), "BLUE": (30, 30, 200), "CYAN": (0, 200, 200)}


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
        # The grid coordinate is the mouse is currently over.
        self.moused_tile: GridPoint | None = None

    def get_name(self):
        return "Grid"

    def pixels_to_grid(self, point: Point) -> GridPoint:
        """Return Grid coordinate of point in pixels."""
        return GridPoint(int(point.x // self.cell_size), int(point.y // self.cell_size))

    def grid_to_pixels(self, grid_point: Point) -> Point:
        return Point(grid_point.x * self.cell_size, grid_point.y * self.cell_size)

    def draw_line(self, start: Point, end: Point, color=common_colours["BLUE"], line_width=2):
        pygame.draw.line(self.surface, color, start, end, line_width)

    def draw_box(self, start: Point, size: Point | None = None, color=common_colours["CYAN"]):
        size = size or Point(self.cell_size, self.cell_size)
        width = Point(size.x, 0)
        height = Point(0, size.y)

        def draw_line(s: Point, e: Point):
            self.draw_line(start=s, end=e, color=color)

        draw_line(start, start + width)
        draw_line(start, start + height)
        draw_line(start + width, start + size)
        draw_line(start + height, start + size)

    def draw_grid_surface(self):
        """Draw grid lines."""
        max_x, max_y = self.surface.get_size()
        for x in range(0, max_x, self.cell_size):
            self.draw_line(Point(x, 0), Point(x, max_y))

        for y in range(0, max_y, self.cell_size):
            self.draw_line(Point(0, y), Point(max_x, y))

        self.draw_line(Point(0, max_y), Point(max_x, max_y))
        self.draw_line(Point(max_x, 0), Point(max_x, max_y))

    def draw_cursor(self):
        self.draw_box(self.grid_to_pixels(self.moused_tile))

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
        if self.moused_tile:
            self.draw_cursor()
        self.draw_tiles()
        return self.surface


class World(Surface):
    default_grid_size = GridPoint(5, 7)

    def __init__(self, width: int, height: int, grid_size: GridPoint = default_grid_size, cell_size: int = 50):
        assert grid_size.x * cell_size < width, "Grid too wide for display area!"
        assert grid_size.y * cell_size < height, "Grid too tall for display area!"
        self.name = "World"
        self.grid = Grid(grid_size)
        self.grid[self.grid.size.x // 2, self.grid.size.y // 2].contains = Base
        self.render_grid = RenderGrid(self.grid, cell_size)
        self.world_surface = pygame.Surface((width, height))

    def update(self, mouse_position: Point | None):
        if mouse_position:
            moused_tile = self.render_grid.pixels_to_grid(mouse_position - Point(*self.get_render_grid_rect()[:2]))
            if self.grid.is_in_grid(moused_tile):
                self.render_grid.moused_tile = moused_tile
                return
        self.render_grid.moused_tile = None

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
        self.add_building(WardenOutpost, grid_coord)

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

    def validate_schematic(self, schematic: Grid, subgrid: Grid):
        logging.info(f"Schem {schematic.size}")
        logging.info(f"Subgrid {subgrid.size}")

        for schematic_tile, grid_tile in zip(schematic, subgrid):
            logging.info(f"Schem Tile {schematic_tile}")
            logging.info(f"Subgrid Tile {grid_tile}")

    def add_building(self, building: Building, location: GridPoint):
        """Checks wheter a building can be done then places the building"""
        schematic = building.schematic
        subgrid = self.grid.get_subgrid(location.x, location.y, schematic.size.x, schematic.size.y)
        self.validate_schematic(schematic, subgrid)

        # Check for validity
        # Asks for building
        # Removes resources
        # Places building
