"""

"""

from __future__ import annotations

import logging
from typing import Type

import pygame

from buildings import Base, Building
from cursor import CursorStates, cursor
from grid import Grid
from helpers import ORTHOGONAL, Box, Event, GridPoint, Notify, Point
from resources import Queue, Resource
from score import score
from templates import Surface
from thing import Thing

common_colours = {
    "BLACK": (0, 0, 0),
    "WHITE": (200, 200, 200),
    "BLUE": (30, 30, 200),
    "CYAN": (0, 200, 200),
    "GREEN": (0, 200, 0),
    "RED": (200, 0, 0),
    "GREY": (100, 100, 100),
}


class RenderGrid(Surface):
    def __init__(self, grid: Grid, cell_size: int):
        self.cell_size = cell_size
        self.grid = grid
        surface_size = Point(self.grid.width * self.cell_size, self.grid.height * self.cell_size)
        self.surface = pygame.Surface(surface_size)
        # The grid coordinate is the mouse is currently over.
        self.moused_tile: GridPoint | None = None

    def process_inputs(self, mouse_position: Point):
        # This is handled by World
        pass

    def get_name(self):
        return "Grid"

    def pixels_to_grid(self, point: Point) -> GridPoint:
        """Return Grid coordinate of point in pixels."""
        return GridPoint(int(point.x // self.cell_size), int(point.y // self.cell_size))

    def grid_to_pixels(self, grid_point: Point) -> Point:
        return Point(grid_point.x * self.cell_size, grid_point.y * self.cell_size)

    def draw_line(self, start: Point, end: Point, color=common_colours["BLUE"], line_width=2):
        pygame.draw.line(self.surface, color, start, end, line_width)

    def draw_box(self, start: Point, size: Point | None = None, color=common_colours["BLUE"], width=1):
        # If width is 0 then the box will be filled.
        size = size or Point(self.cell_size, self.cell_size)
        pygame.draw.rect(self.surface, color, (*start, *size), width=width)

    def draw_grid_surface(self, ignore_empty=False):
        """Draw grid lines."""
        for pos, tile in self.grid:
            if ignore_empty and tile.empty:
                continue
            self.draw_box(self.grid_to_pixels(pos), color=common_colours["BLACK"], width=0)
            self.draw_box(self.grid_to_pixels(pos), color=common_colours["BLUE"])

    def draw_schematic(self, cursor_location: GridPoint, color: tuple[int, int, int]):
        for pos, tile in cursor.get_shape():
            if tile.empty:
                continue
            location = cursor_location + pos
            self.draw_box(self.grid_to_pixels(location), color=color, width=3)

    def draw_cursor(self):
        color = common_colours["CYAN"]
        cursor_location: GridPoint = self.moused_tile
        match cursor.get_state():
            case CursorStates.RESOURCE_PLACE:
                color = common_colours["CYAN"]
                self.draw_schematic(cursor_location, color)

            case CursorStates.BUILD_OUTLINE:
                if self.grid.is_in_grid(self.moused_tile + cursor.get_shape().size - GridPoint(1, 1)):
                    subgrid, _offset = self.grid.get_subgrid(*self.moused_tile, *cursor.get_shape().size)
                    if validate_schematic(cursor.get_shape(), subgrid):
                        color = common_colours["GREEN"]
                else:
                    color = common_colours["RED"]
                self.draw_schematic(cursor_location, color)

            case CursorStates.BUILD_LOCATION:
                cursor_location = cursor.get_building_location()
                color = common_colours["GREEN"]
                self.draw_schematic(cursor_location, color)
                cursor_colour = common_colours["GREY"]
                self.draw_box(self.grid_to_pixels(self.moused_tile), color=cursor_colour, width=5)
            case _:
                logging.error("Error: Cursor in invalid state")

    def draw_tile(self, thing: Type[Thing], grid_coord: GridPoint):
        scaled = pygame.transform.scale(thing.image(), (self.cell_size // 1.5, self.cell_size // 1.5))
        asset_size = Point(*scaled.get_size())
        self.surface.blit(
            scaled,
            (
                (grid_coord.x + 0.5) * self.cell_size - asset_size.x // 2,
                (grid_coord.y + 0.5) * self.cell_size - asset_size.y // 2,
            ),
        )

    def draw_tiles(self):
        for point, tile in self.grid:
            if thing := tile.contains:
                self.draw_tile(thing, point)

    def render(self, ignore_empty=False, background_color=common_colours["BLUE"]) -> pygame.Surface:
        self.surface.fill(background_color)
        self.draw_grid_surface(ignore_empty)
        if self.moused_tile:
            self.draw_cursor()
        self.draw_tiles()
        return self.surface


def validate_schematic(schematic: Grid, subgrid: Grid) -> bool:
    # Add check for in grid
    for (_, schematic_tile), (_, grid_tile) in zip(schematic, subgrid, strict=True):
        if schematic_tile.empty or schematic_tile.contains == grid_tile.contains:
            pass
        else:
            return False
    return True


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
        cursor_state = cursor.get_state()
        # Fails if clicked elsewhere on the canvas.
        if self.grid.is_in_grid(grid_coord):
            match cursor_state:
                case CursorStates.RESOURCE_PLACE:
                    resource = Queue.peek()
                    if self.fill_tile(grid_coord, resource):
                        Queue.take()
                        Notify(Event.PlaceResource)
                case CursorStates.BUILD_OUTLINE:
                    self.add_building(grid_coord)
                case CursorStates.BUILD_LOCATION:
                    self.confirm_building(grid_coord)
                case _:
                    logging.error("No state exists for the current cursor state!")

    def render(self) -> pygame.Surface:
        """Blit the grid to the center of the canvas."""
        self.world_surface.fill(common_colours["BLACK"])

        grid = self.render_grid.render()

        x, y, width, height = self.get_render_grid_rect()
        pygame.draw.rect(self.world_surface, common_colours["BLUE"], (x - 1, y - 1, width + 2, height + 2))

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

    def calculate_score(self):
        world_score = 0
        for _pos, tile in self.grid:
            if tile.contains:
                if tile.contains.score:
                    world_score += tile.contains.score
        score.score = world_score

    def add_building(self, location: GridPoint):
        """Checks whether a building can be build with selected resources"""
        schematic = cursor.get_shape()
        if self.grid.is_in_grid(location + schematic.size - GridPoint(1, 1)):
            subgrid, offset = self.grid.get_subgrid(location.x, location.y, schematic.size.x, schematic.size.y)
            if validate_schematic(schematic, subgrid):
                cursor.set_state(CursorStates.BUILD_LOCATION)
                cursor.set_building_location(offset)
                return
        else:
            logging.warning("Illegal move: Build schematic does not fit in map")
        cursor.set_state(CursorStates.RESOURCE_PLACE)
        cursor.set_building(None)
        cursor.set_building_location(None)
        return

    def remove_things_in_schematic(self, schematic: Grid):
        schematic = cursor.get_shape()
        offset = cursor.get_building_location()
        for row in range(schematic.size.y):
            for column in range(schematic.size.x):
                if schematic[column, row].contains:
                    self.grid[column + offset.x, row + offset.y].contains = None

    def confirm_building(self, location: GridPoint):
        schematic = cursor.get_shape()
        offset = cursor.get_building_location()
        # Maintain outline
        valid_range = Box(
            offset.x,
            offset.y,
            schematic.size.x,
            schematic.size.y,
        )
        if valid_range.contains(location):
            if self.grid[location].contains:
                self.remove_things_in_schematic(schematic)
                self.grid[location].contains = cursor.get_building()
                self.calculate_score()

        cursor.set_state(CursorStates.RESOURCE_PLACE)
        cursor.set_building(None)
        cursor.set_building_location(None)
