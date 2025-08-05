"""

"""

from __future__ import annotations

import importlib.resources
import logging
from enum import Enum
from typing import Type

import pygame as pg

import config
from tiny_space import buildings
from tiny_space.buildings import Building
from tiny_space.cursor import CursorStates, cursor
from tiny_space.grid import Grid
from tiny_space.helpers import ORTHOGONAL, Event, GridPoint, Notifier, Point
from tiny_space.resources import Queue, Resource
from tiny_space.score import score
from tiny_space.templates import GraphicsComponent
from tiny_space.thing import Nothing, Thing


class Color(tuple, Enum):
    BLACK = (0, 0, 0)
    WHITE = (200, 200, 200)
    BLUE = (30, 30, 200)
    CYAN = (0, 200, 200)
    GREEN = (0, 200, 0)
    RED = (200, 0, 0)
    GREY = (100, 100, 100)
    DARK_GREY = (50, 50, 50)


class WorldGraphicsComponent(GraphicsComponent):
    """Handles the world surface and drawing to it."""

    def __init__(self, size: Point | int, grid_size: GridPoint, schematic: bool = False):
        """Size[Point] is the dimensions of the surface. Size[int] is the size of each grid tile."""
        if isinstance(size, int):
            self.cell_size = size
        else:
            self.cell_size = self.calculate_cell_size(size, grid_size)
        self.surface = pg.Surface(grid_size * self.cell_size)

        root_asset_dir = str(importlib.resources.files(__package__))
        self.hammer_assets = [
            pg.image.load(f"{root_asset_dir}/assets/hammer/hammer1.png"),
            pg.image.load(f"{root_asset_dir}/assets/hammer/hammer2.png"),
            pg.image.load(f"{root_asset_dir}/assets/hammer/hammer3.png"),
            pg.image.load(f"{root_asset_dir}/assets/hammer/hammer4.png"),
            pg.image.load(f"{root_asset_dir}/assets/hammer/hammer5.png"),
        ]
        self.frame_count = 0
        # Schematic mode: disable interactivity for schematic book sidebar display.
        self.schematic = schematic

    @staticmethod
    def calculate_cell_size(size: Point, grid_size: GridPoint) -> int:
        max_grid_size_px = size * 9 // 10
        return min(max_grid_size_px.x // grid_size.x, max_grid_size_px.y // grid_size.y)

    def pixels_to_grid(self, point: Point) -> GridPoint:
        """Convert pixel coordinate to grid coordinate."""
        return GridPoint(int(point.x // self.cell_size), int(point.y // self.cell_size))

    def grid_to_pixels(self, grid_point: GridPoint) -> Point:
        """Convert grid coordinate to pixel coordinate"""
        return Point(grid_point.x * self.cell_size, grid_point.y * self.cell_size)

    # def draw_line(self, start: Point, end: Point, color=Color.BLUE, line_width=2):
    #     line_width = line_width * config.SCALE
    #     pg.draw.line(self.surface, color, start, end, line_width)

    def draw_box(self, start: Point, size: Point | None = None, color=Color.BLUE, width=1):
        # If width is 0 then the box will be filled.
        size = size or Point(self.cell_size, self.cell_size)
        pg.draw.rect(self.surface, color, (*start, *size), width=width * config.SCALE)

    def draw_grid_surface(self, grid: Grid, skip_nothing: bool = False):
        """Draw tile outlines. Use ignore_empty to draw outlines of full tiles."""
        for pos, tile in grid:
            if skip_nothing and tile is Nothing:
                continue
            self.draw_box(self.grid_to_pixels(pos), color=Color.BLACK, width=0)
            self.draw_box(self.grid_to_pixels(pos), color=Color.BLUE)

    def get_moused_tile(self, mouse_coord: Point) -> GridPoint | None:
        if self.surface.get_rect().collidepoint(mouse_coord):
            return self.pixels_to_grid(mouse_coord)
        return None

    def _draw_cursor(self, grid: Grid, cursor_location: GridPoint, shape: Grid, color=Color.CYAN, width=3):
        """Draw the shape under Cursor at cursor_location.

        TODO: Merge this with draw_grid_surface and hold cursor state in Cursor?
        """
        for pos, tile in shape:
            if tile is Nothing:
                continue
            location = cursor_location + pos
            if not grid.is_in_grid(location):
                continue
            self.draw_box(self.grid_to_pixels(location), color=color, width=width)

    def draw_build_hammers(self):
        if shadow := cursor.get_shadow_shape():
            shadow_location = cursor.get_building_location()
            if not shadow_location:
                return
            for pos, tile in shadow:
                if tile is Nothing:
                    continue
                location = shadow_location + pos
                scaled = pg.transform.scale_by(self.hammer_assets[(self.frame_count // 6) % 5], config.SCALE)
                size = Point(*scaled.get_size())
                self.surface.blit(
                    scaled,
                    (
                        (location.x + 0.5) * self.cell_size - size.x // 2,
                        (location.y + 0.5) * self.cell_size - size.y // 2,
                    ),
                )

    def draw_cursor(self, grid: Grid, mouse_pos: Point):
        # TODO: Make this method less ugly.
        if shadow := cursor.get_shadow_shape():
            shadow_location = cursor.get_building_location()
            assert shadow_location
            # TODO: Add arrows pointing at the cursor tiles (They're valid build placements)
            self._draw_cursor(grid, shadow_location, shadow, Color.GREEN)

        if moused_tile := self.get_moused_tile(mouse_pos):
            cursor_color = Color.CYAN
            if cursor.get_state() == CursorStates.BUILD_OUTLINE:
                if grid.is_in_grid(moused_tile + cursor.get_shape().size - GridPoint(1, 1)):
                    subgrid, _offset = grid.get_subgrid(*moused_tile, *cursor.get_shape().size)
                    if validate_schematic(cursor.get_shape(), subgrid):
                        cursor_color = Color.GREEN
                else:
                    cursor_color = Color.RED
            elif cursor.get_state() == CursorStates.BUILD_LOCATION:
                cursor_color = Color.GREY
            self._draw_cursor(grid, moused_tile, cursor.get_shape(), cursor_color)

    def draw_tile(self, thing: Type[Thing] | Type[Nothing], grid_coord: GridPoint):
        if image := thing.image():
            scaled = pg.transform.scale_by(image, config.SCALE)
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
            self.draw_tile(tile, point)

    def render(self, grid: Grid, mouse_pos: Point = Point(-1, -1), background_color=Color.BLUE) -> pg.Surface:
        self.surface.fill(background_color)
        self.draw_grid_surface(grid, skip_nothing=self.schematic)
        if not self.schematic:
            self.draw_cursor(grid, mouse_pos)
        self.draw_tiles(grid)
        if not self.schematic:
            self.draw_build_hammers()
        self.frame_count += 1
        return self.surface


def validate_schematic(schematic: Grid, subgrid: Grid) -> bool:
    return not any(
        schematic_tile is not Nothing and schematic_tile != grid_tile
        for (_, schematic_tile), (_, grid_tile) in zip(schematic, subgrid, strict=True)
    )


class World(GraphicsComponent):
    default_grid_size = GridPoint(5, 7)

    def __init__(self, size: Point, grid_size: GridPoint = default_grid_size):
        self.grid = Grid.from_dimensions(grid_size)
        self.grid[self.grid.size // 2] = buildings.Base
        self.graphics = WorldGraphicsComponent(size, grid_size)

    @property
    def surface(self):
        return self.graphics.surface

    def process_inputs(self, mouse_position: Point):
        moused_tile = self.graphics.pixels_to_grid(mouse_position)
        match cursor.get_state():
            case CursorStates.RESOURCE_PLACE:
                resource = Queue.peek()
                if self.fill_tile(moused_tile, resource):
                    Queue.take()
                    Notifier.notify(Event.PlaceResource)
            case CursorStates.BUILD_OUTLINE:
                self.lock_build_outline(moused_tile)
            case CursorStates.BUILD_LOCATION:
                self.confirm_building(moused_tile)

    def render(self, mouse_pos: Point) -> pg.Surface:
        """Blit the grid to the center of the canvas."""
        return self.graphics.render(self.grid, mouse_pos)

    def has_adjacent_tile(self, grid_coord: GridPoint) -> bool:
        """Returns True if an adjacent tile isn't empty."""
        orthogonal_tiles: list[GridPoint] = [grid_coord + direction for direction in ORTHOGONAL]
        return any(self.grid.is_in_grid(point) and self.grid[point] is not Nothing for point in orthogonal_tiles)

    def fill_tile(self, point: GridPoint, thing: Type[Resource] | Type[Building]) -> bool:
        """Fill the tile, if possible.

        Filling a tile is not possible if it's already filled or if there are no adjacent filled tiles.
        """
        if self.grid[point] is not Nothing:
            logging.warning(f"Illegal move: Can't fill occupied tile at {point}.")
            return False
        if not self.has_adjacent_tile(point):
            logging.warning(f"Illegal move: Can't fill disconnected tile at {point}.")
            return False
        self.grid[point] = thing
        return True

    def calculate_score(self):
        score.score = sum(tile.score for _pos, tile in self.grid)

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
        assert schematic
        offset = cursor.get_building_location()
        assert offset
        for pos, item in schematic:
            if item is not Nothing:
                self.grid[pos + offset] = Nothing

    def confirm_building(self, location: GridPoint):
        schematic = cursor.get_shadow_shape()
        assert schematic
        offset = cursor.get_building_location()
        assert offset
        # Maintain outline
        valid_range = pg.Rect(
            offset.x,
            offset.y,
            schematic.size.x,
            schematic.size.y,
        )
        if valid_range.collidepoint(location) and schematic[location - offset] is not Nothing:
            self.remove_things_in_schematic()
            self.grid[location] = cursor.get_building() or Nothing
            self.calculate_score()
        else:
            logging.warning("Invalid building placement, returning to resource placement.")
        cursor.set_state(CursorStates.RESOURCE_PLACE)
