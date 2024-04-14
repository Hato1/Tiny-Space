"""

"""


from __future__ import annotations

import itertools
import logging
from enum import Enum
from typing import Type

import pygame

from buildings import Base, Building
from cursor import CursorStates, cursor
from grid import Grid
from helpers import ORTHOGONAL, Box, Event, GridPoint, Notify, Point
from resources import Queue, Resource
from score import score
from templates import Surface, SurfaceInputComponent
from thing import Thing


class Colour(tuple, Enum):
    BLACK = (0, 0, 0)
    WHITE = (200, 200, 200)
    BLUE = (30, 30, 200)
    CYAN = (0, 200, 200)
    GREEN = (0, 200, 0)
    RED = (200, 0, 0)
    GREY = (100, 100, 100)


class WorldGraphicsComponent(Surface):
    """Handles the world surface and drawing to it."""

    def __init__(self, grid_size: GridPoint, cell_size: int):
        self.cell_size = cell_size
        self.surface = pygame.Surface(grid_size * cell_size)
        self.box = Box(*self.surface.get_rect())
        self.hammer_assets = [
            pygame.image.load("assets/hammer/hammer1.png"),
            pygame.image.load("assets/hammer/hammer2.png"),
            pygame.image.load("assets/hammer/hammer3.png"),
            pygame.image.load("assets/hammer/hammer4.png"),
            pygame.image.load("assets/hammer/hammer5.png"),
        ]
        self.frame_count = 0

    def center_box(self, box):
        """Set self.box position to be in the center of box."""
        assert self.surface.get_width() < box.width, "Grid too wide for display area!"
        assert self.surface.get_height() < box.height, "Grid too tall for display area!"
        self.box = Box(*self.surface.get_rect(center=box.center))

    def pixels_to_grid(self, point: Point) -> GridPoint:
        """Convert pixel coordinate to grid coordinate."""
        return GridPoint(int(point.x // self.cell_size), int(point.y // self.cell_size))

    def grid_to_pixels(self, grid_point: GridPoint) -> Point:
        """Convert grid coordinate to pixel coordinate"""
        return Point(grid_point.x * self.cell_size, grid_point.y * self.cell_size)

    def draw_line(self, start: Point, end: Point, color=Colour.BLUE, line_width=2):
        pygame.draw.line(self.surface, color, start, end, line_width)

    def draw_box(self, start: Point, size: Point | None = None, color=Colour.BLUE, width=1):
        # If width is 0 then the box will be filled.
        size = size or Point(self.cell_size, self.cell_size)
        pygame.draw.rect(self.surface, color, (*start, *size), width=width)

    def draw_grid_surface(self, grid: Grid):
        """Draw tile outlines. Use ignore_empty to draw outlines of full tiles."""
        for pos, tile in grid:
            if tile.invisible:
                continue
            self.draw_box(self.grid_to_pixels(pos), color=Colour.BLACK, width=0)
            self.draw_box(self.grid_to_pixels(pos), color=Colour.BLUE)

    def get_moused_tile(self) -> GridPoint | None:
        mouse_coord = Point(*pygame.mouse.get_pos())
        if relative := mouse_coord.relative_to(self.box):
            return self.pixels_to_grid(relative)
        return None

    def _draw_cursor(self, grid: Grid, cursor_location: GridPoint, shape, color=Colour.CYAN, width=3):
        """Draw the shape under Cursor at cursor_location.

        TODO: Merge this with draw_grid_surface and hold cursor state in Cursor?
        """
        if not cursor_location:
            return
        for pos, tile in shape:
            if tile.empty:
                continue
            location = cursor_location + pos
            if not grid.is_in_grid(location):
                continue
            if grid[location[0], location[1]].invisible:
                continue
            self.draw_box(self.grid_to_pixels(location), color=color, width=width)

    def draw_build_hammers(self):
        if shadow := cursor.get_shadow_shape():
            shadow_location = cursor.get_building_location()
            if not shadow_location:
                return
            for pos, tile in shadow:
                if tile.empty:
                    continue
                location = shadow_location + pos
                size = Point(*self.hammer_assets[0].get_size())
                self.surface.blit(
                    self.hammer_assets[(self.frame_count // 6) % 5],
                    (
                        (location.x + 0.5) * self.cell_size - size.x // 2,
                        (location.y + 0.5) * self.cell_size - size.y // 2,
                    ),
                )

    def draw_cursor(self, grid: Grid):
        # TODO: Make this method less ugly.
        if shadow := cursor.get_shadow_shape():
            shadow_location = cursor.get_building_location()
            # TODO: Add arrows pointing at the cursor tiles (They're valid build placements)
            self._draw_cursor(grid, shadow_location, shadow, Colour.GREEN)

        if moused_tile := self.get_moused_tile():
            cursor_color = Colour.CYAN
            if cursor.get_state() == CursorStates.BUILD_OUTLINE:
                if grid.is_in_grid(moused_tile + cursor.get_shape().size - GridPoint(1, 1)):
                    subgrid, _offset = grid.get_subgrid(*moused_tile, *cursor.get_shape().size)
                    if validate_schematic(cursor.get_shape(), subgrid):
                        cursor_color = Colour.GREEN
                else:
                    cursor_color = Colour.RED
            elif cursor.get_state() == CursorStates.BUILD_LOCATION:
                cursor_color = Colour.GREY
                # width=5
            self._draw_cursor(grid, moused_tile, cursor.get_shape(), cursor_color)

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

    def draw_tiles(self, grid: Grid):
        for point, tile in grid:
            if thing := tile.contains:
                self.draw_tile(thing, point)

    def render(self, grid: Grid, ignore_empty: bool = False, background_color=Colour.BLUE) -> pygame.Surface:
        self.surface.fill(background_color)
        self.draw_grid_surface(grid)
        self.draw_cursor(grid)
        self.draw_tiles(grid)
        self.draw_build_hammers()
        self.frame_count += 1
        return self.surface


def validate_schematic(schematic: Grid, subgrid: Grid) -> bool:
    return not any(
        not schematic_tile.empty
        and schematic_tile.contains != grid_tile.contains
        for (_, schematic_tile), (_, grid_tile) in zip(
            schematic, subgrid, strict=True
        )
    )


class WorldInputComponent(SurfaceInputComponent):
    pass


class World(Surface):
    default_grid_size = GridPoint(5, 7)

    def __init__(self, grid_size: GridPoint = default_grid_size, cell_size: int = 50):
        self.grid = Grid(grid_size)
        self.grid[self.grid.size.x // 2, self.grid.size.y // 2].contains = Base
        self.graphics = WorldGraphicsComponent(grid_size, cell_size)
        self.input = WorldInputComponent()

    @property
    def box(self):
        return self.graphics.box

    def update(self):
        pass

    def process_inputs(self, mouse_position: Point):
        moused_tile = self.graphics.pixels_to_grid(mouse_position)
        match cursor.get_state():
            case CursorStates.RESOURCE_PLACE:
                resource = Queue.peek()
                if self.fill_tile(moused_tile, resource):
                    Queue.take()
                    Notify(Event.PlaceResource)
            case CursorStates.BUILD_OUTLINE:
                self.lock_build_outline(moused_tile)
            case CursorStates.BUILD_LOCATION:
                self.confirm_building(moused_tile)

    def render(self) -> pygame.Surface:
        """Blit the grid to the center of the canvas."""
        return self.graphics.render(self.grid)

    def has_adjacent_tile(self, grid_coord: GridPoint) -> bool:
        """Returns True if an adjacent tile isn't empty."""
        orthogonal_tiles: list[GridPoint] = [grid_coord + direction for direction in ORTHOGONAL]
        return any(
            self.grid.is_in_grid(point) and not self.grid[point].empty
            for point in orthogonal_tiles
        )

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
        score.score = sum(
            tile.contains.score
            for _pos, tile in self.grid
            if not tile.empty and tile.contains.score
        )

    def lock_build_outline(self, location: GridPoint):
        """Checks whether a building can be build with selected resources"""
        schematic = cursor.get_shape()
        if self.grid.is_in_grid(location + schematic.size - GridPoint(1, 1)):
            subgrid, offset = self.grid.get_subgrid(location.x, location.y, schematic.size.x, schematic.size.y)
            if validate_schematic(schematic, subgrid):
                cursor.set_state(CursorStates.BUILD_LOCATION, location=offset)
                return
        else:
            logging.warning("Illegal move: Build schematic does not fit in map")
        cursor.set_state(CursorStates.RESOURCE_PLACE)
        return

    def remove_things_in_schematic(self):
        schematic = cursor.get_shadow_shape()
        offset = cursor.get_building_location()
        for row, column in itertools.product(range(schematic.size.y), range(schematic.size.x)):
            if schematic[column, row].contains:
                self.grid[column + offset.x, row + offset.y].contains = None

    def confirm_building(self, location: GridPoint):
        schematic = cursor.get_shadow_shape()
        offset = cursor.get_building_location()
        # Maintain outline
        valid_range = Box(
            offset.x,
            offset.y,
            schematic.size.x,
            schematic.size.y,
        )
        # FIXME: Replace empty check with check that build location is in cursor schematic.
        #  Otherwise you can build atop of any tile.
        if location in valid_range and not self.grid[location].empty:
            self.remove_things_in_schematic()
            self.grid[location].contains = cursor.get_building()
            self.calculate_score()
        cursor.set_state(CursorStates.RESOURCE_PLACE)
